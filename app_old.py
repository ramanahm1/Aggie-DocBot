# Imports
# 1. Streamlit
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

# 2. Langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain

# 3. PDF Reading
from PyPDF2 import PdfReader

# 4. Python Object Disc Store
import pickle

# 5. Load Environment Variables
from dotenv import load_dotenv

# 6. Google Drive Utils
from utils.gdrive_utils import authenticate_gdrive, list_files_in_folder, download_file_from_drive, upload_file_to_drive

# 7. Database Utils
from utils.db_utils import create_connection, get_all_documents

# 7. Generic Utils
import os

###################################################################################################
### Code Start

# Database settings
database = "documents.db"
conn = create_connection(database)

# UI
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

def initiate_sidebar():
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

# All Functionality
def main():
  # Load Environment Variables
  load_dotenv()

  # Google API Key
  google_api_key = os.getenv('GOOGLE_API_KEY')

  if not google_api_key:
    raise ValueError("API key not found. Please set it in the .env file.")
  
  # UI
  initiate_sidebar()

  # UI: Header
  st.header('Aggie-DocBot')
  
  # File Upload
  pdf = st.file_uploader('Upload your PDF')

  # PDF Reading, Chunking, VectoreStore
  if pdf is not None:
    pdf_reader = PdfReader(pdf)
    pdf_name = pdf.name

    text = ""
    for page in pdf_reader.pages:
      text += page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(
      chunk_size = 1000,
      chunk_overlap = 200,
      length_function = len
    )

    chunks = text_splitter.split_text(text=text)
    store_name = pdf_name[:-4]

    if os.path.exists(f"{'embedding_store'/store_name}.pkl"):
      with open(f"{store_name}.pkl", "rb") as f:
        VectorStore = pickle.load(f)
      st.write("File exists, embeddings loaded from disk.")
    else:
      embeddings = HuggingFaceEmbeddings()
      VectorStore = FAISS.from_texts(chunks, embedding = embeddings)
      with open(f"{store_name}.pkl", "wb") as f:
        pickle.dump(VectorStore, f)
    
    query = st.text_input("Ask anything about your PDF!")

    if query:
      docs = VectorStore.similarity_search(query=query, k=3)
      llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
      chain = load_qa_chain(llm=llm, chain_type="stuff")
      response = chain.run(input_documents=docs, question=query)
      st.write(response)

if __name__ == "__main__":
  main()
