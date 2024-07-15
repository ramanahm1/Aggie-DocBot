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

# 6. Utils
import os


### Code Start

# UI
with st.sidebar:
  st.title("Docs Show Up Here")

# All Functionality
def main():
  # Load Environment Variables
  load_dotenv()

  # Google API Key
  google_api_key = os.getenv('GOOGLE_API_KEY')

  if not google_api_key:
    raise ValueError("API key not found. Please set it in the .env file.")

  # UI: Header
  st.header('Aggie-DocBot')
  
  # File Upload
  pdf = st.file_uploader('STEP 1: Upload your PDF')

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

    if os.path.exists(f"{store_name}.pkl"):
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