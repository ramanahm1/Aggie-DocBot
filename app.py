# Imports
# 1. Streamlit
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

# 2. Langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# 3. PDF Reading
from PyPDF2 import PdfReader

# 4. Python Object Disc Store
import pickle


### Code Start

# UI
with st.sidebar:
  st.title("Docs Show Up Here")

# All Functionality
def main():
  # UI: Header
  st.header('Aggie-DocBot')
  
  # File Upload
  pdf = st.file_uploader('STEP 1: Upload your PDF')
  pdf_name = pdf.name

  # PDF Reading, Chunking, VectoreStore
  if pdf is not None:
    pdf_reader = PdfReader(pdf)

    text = ""
    for page in pdf_reader.pages:
      text += page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(
      chunk_size = 1000,
      chunk_overlap = 200,
      length_function = len
    )

    chunks = text_splitter.split_text(text=text)
    embeddings = HuggingFaceEmbeddings()
    VectorStore = FAISS.from_texts(chunks, embedding = embeddings)
    store_name = pdf_name[:-4]
    with open(f"{store_name}.pkl", "wb") as f:
      print("Foo")
      
    # st.write(chunks)

if __name__ == "__main__":
  main()