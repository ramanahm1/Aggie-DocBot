from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import pickle
from dotenv import load_dotenv
import getpass
import os

def save_load_faiss_embeddings():
  chunks = [
    'Hello',
    'How are you?',
    'Texas A&M',
    'College Station',
    'Hedwig'
  ]
  embeddings = [
    [0.1, 0.002, 0.7, 0.5],
    [0.5, 0.1, 0.065, 0.56],
    [0.1, 0.1, 0.1, 0.9],
    [0.45, 0.23, 0.16, 0.98],
    [0.99, 0.89, 0.79, 0.69]
  ]
  zipped_embeddings = list(zip(chunks, embeddings))
  

  vector_store = FAISS.from_embeddings(zipped_embeddings, embeddings)
  print("$$$$$$ Created vector store")

  vector_store.save_local('embedding_store', index_name='samp_vector_index')
  print("$$$$$$ Saved vector store")

  v_c = FAISS.load_local(folder_path='embedding_store', embeddings=embeddings, index_name='samp_vector_index', allow_dangerous_deserialization=True)
  print("$$$$$$ Loaded vector store")


def save_embeddings():
  embeddings = [
    [0.1, 0.002, 0.7, 0.5],
    [0.5, 0.1, 0.065, 0.56],
    [0.1, 0.1, 0.1, 0.9],
    [0.45, 0.23, 0.16, 0.98],
    [0.99, 0.89, 0.79, 0.69]
  ]
  store_name = 'foo'
  with open(f'embedding_store/{store_name}_embeddings.pkl', 'wb') as file:
    pickle.dump(embeddings, file)

def load_embeddings():
  store_name = 'foo'
  with open(f'embedding_store/{store_name}_embeddings.pkl', 'rb') as file:
      loaded_list = pickle.load(file)
      print(loaded_list)




# k = zip(['a', 'b', 'c'], [1, 2, 3])
# for i in k:
#   print(i)
#save_load_faiss_embeddings()
save_embeddings()
load_embeddings()

