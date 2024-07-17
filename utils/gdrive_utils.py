from googleapiclient.discovery import build
from google.oauth2 import service_account
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from dotenv import load_dotenv
import os
import time

def authenticate_gdrive():
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    SERVICE_ACCOUNT_FILE = '/Users/ramana/Documents/RAG PDF Chat/secrets/arctic-sentry-425004-f9-d134b7a0df00.json'

    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('drive', 'v3', credentials=creds)
    return service

def list_files_in_folder(folder_id):
    try:
        print(f"Listing files in folder ID: {folder_id}")
        service = authenticate_gdrive()
        print("Service created.")
        
        results = []
        page_token = None
        
        while True:
            response = service.files().list(
                q=f"'{folder_id}' in parents",
                pageSize=1000,
                fields="nextPageToken, files(id, name)",
                pageToken=page_token
            ).execute()
            
            items = response.get('files', [])
            results.extend(items)
            
            page_token = response.get('nextPageToken')
            if not page_token:
                break

        if not results:
            print("No files found.")
        else:
            print(f"Found {len(results)} files.")
        
        return results
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Download a file from Google Drive
def download_file_from_drive(file_id, file_name):
    service = authenticate_gdrive()
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_name, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

# Upload a file to Google Drive
def upload_file_to_drive(uploaded_file, folder_id):
    service = authenticate_gdrive()
    file_metadata = {
        'name': uploaded_file.name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(uploaded_file, mimetype=uploaded_file.type)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"File ID: {file.get('id')}")

# Main function
def main():
    load_dotenv()
    print(os.getenv('GDRIVE_DOC_STORE_ID'))
    folder_id = os.getenv('GDRIVE_DOC_STORE_ID')

    # List files
    files = list_files_in_folder(folder_id)
    print("Files in folder:", files)

    # # Download a file example
    # if files:
    #     first_file_id = files[0]['id']
    #     first_file_name = files[0]['name']
    #     download_file_from_drive(first_file_id, first_file_name)

    # # Upload a file example
    # file_path = 'path/to/your/upload_file.pdf'  # Replace with your file path
    # upload_file_to_drive(file_path, folder_id)

if __name__ == "__main__":
    main()