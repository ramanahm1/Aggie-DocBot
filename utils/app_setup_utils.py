import streamlit as st
from utils.gdrive_utils import list_files_in_folder, download_file_from_drive
from utils.db_utils import get_all_documents
import os

def include_context_button(selected_uuids, pdf_name_index):
    if st.sidebar.button('Include Context', disabled=not selected_uuids):
        st.write("Button pressed")

        # Get Google file IDs and file names from Google Drive
        g_drive_files = list_files_in_folder(os.getenv('GDRIVE_DOC_STORE_ID'))
        g_drive_pickles = {val['id']: val['name'] for val in list_files_in_folder(os.getenv('GDRIVE_EMBEDDINGS_STORE_ID'))}
        for g_pkl_id, g_pkl_name in g_drive_pickles.items():
            item_uuid = g_pkl_name.split('.')[0]
            download_path = f'/Users/ramana/Documents/RAG PDF Chat/embedding_store/{g_pkl_name}'
            download_file_from_drive(g_pkl_id, download_path)
            # Add embeddings to the overall list
            st.write(f'Added {pdf_name_index[item_uuid]}')

def initiate_sidebar(conn):
    with st.sidebar:
        st.title("Your PDFs from Google Drive")

        # Get pdf names from G-Drive - I need a list with uuid, file names.
        documents = get_all_documents(conn)
        pdf_name_index = {doc[0]: doc[1] for doc in documents}
        has_embedding_index = {doc[0]: doc[2] for doc in documents}

        selected_uuids = []
        for uuid, file_name in pdf_name_index.items():
            if st.sidebar.checkbox(file_name):
                selected_uuids.append(uuid)
        include_context_button(selected_uuids, pdf_name_index)
