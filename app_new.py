# Imports
# Streamlit
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import getpass

# Langchain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain

# PDF Utils
from utils.pdf_utils import pdf_to_vector_index

# Load Environment Variables
from dotenv import load_dotenv

# Google Drive Utils
from utils.gdrive_utils import authenticate_gdrive, list_files_in_folder, download_file_from_drive, upload_file_to_drive

# Database Utils
from utils.db_utils import create_connection, get_all_documents

# App Setup Utils
from utils.app_setup_utils import initiate_sidebar

# Generic Utils
import os

###################################################################################################
### Code Start

# Database settings
database = "documents.db"
conn = create_connection(database)

def save_docs_to_file(chunks, file_path):
    with open(file_path, 'w') as file:
        for chunk in chunks:
            file.write(chunk + '\n---\n')

# All Functionality
def main():
  # Load Environment Variables
  load_dotenv()

  # Google API Key
  google_api_key = os.getenv('GOOGLE_API_KEY')

  load_dotenv()
  google_api_key = os.getenv("GOOGLE_API_KEY")
  if google_api_key:
    os.environ["GOOGLE_API_KEY"] = google_api_key
  else:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API key here")

  embeddings_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

  if not google_api_key:
    raise ValueError("API key not found. Please set it in the .env file.")
  
  # UI
  initiate_sidebar(conn)

  # UI: Header
  st.header('Aggie-DocBot')
  
  # File Upload
  pdf = st.file_uploader('Upload your PDF')

  # PDF Processing
  if pdf is not None:
    pdf_name = pdf.name
    store_name = pdf_name[:-4]
    
    VectorStore = pdf_to_vector_index(pdf, store_name, embeddings_model)
    
    query = st.text_input("Ask anything about your PDF!")

    if query:
      formatted_query = f"""From provided doc, get the context and answer the query: {query}"""
      query_vector = embeddings_model.embed_query(formatted_query)
      docs = VectorStore.similarity_search_by_vector(embedding=query_vector, k=20, fetch_k=50)
      save_docs_to_file([d.page_content for d in docs], 'search_result.txt')
      llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
      chain = load_qa_chain(llm=llm, chain_type="stuff")
      response = chain.run(input_documents=docs, question=query)
      st.write(response)
      #st.write("Check search results")

if __name__ == "__main__":
  main()
