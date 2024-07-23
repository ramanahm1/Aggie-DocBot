from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import pickle
from dotenv import load_dotenv
import getpass
import os

# def load_embeddings_(store_name):
#     with open(f"embedding_store/{store_name}.pkl", "rb") as f:
#         return pickle.load(f)

def save_embeddings(embeddings, store_name):
    with open(f'embedding_store/{store_name}_embeddings.pkl', 'wb') as file:
      pickle.dump(embeddings, file)

def load_embeddings(store_name):
    with open(f'embedding_store/{store_name}_embeddings.pkl', 'rb') as file:
      loaded_embeddings = pickle.load(file)
      return loaded_embeddings
    
def load_faiss_index(store_name, embeddings):
    directory = 'embeddings_store'
    
    # List all files in the directory
    all_items = os.listdir(directory)
    print([item for item in all_items])
    files = [item for item in all_items if os.path.isfile(os.path.join(directory, item))]
    print("Files in the directory:", files)
    
    # Check if the required .faiss file is in the directory
    required_faiss_file = f"{store_name}.faiss"
    if required_faiss_file not in files:
        raise FileNotFoundError(f"Required FAISS file {required_faiss_file} not found in the directory {directory}")


    vector_index = FAISS.load_local(
      folder_path=os.path.join(os.getcwd(), 'embeddings_store'), 
      embeddings=embeddings, 
      index_name=store_name, 
      allow_dangerous_deserialization=True
    )
    return vector_index
  
def save_faiss_index(vector_index, store_name):
   vector_index.save_local('embeddings_store', index_name=store_name)

  
# def save_embeddings(vector_store, store_name):
#     # Save FAISS Embeddings
#     FAISS.save_local(folder_path = 'embedding_store', index_name = store_name)

#     # Redundant code:
#     # with open(f"embedding_store/{store_name}.pkl", "wb") as f:
#     #     pickle.dump(vector_store, f)

def generate_embeddings(chunks, embeddings_model):
    # Loading the API Key
    # load_dotenv()
    # google_api_key = os.getenv("GOOGLE_API_KEY")
    # if google_api_key:
    #   os.environ["GOOGLE_API_KEY"] = google_api_key
    # else:
    #   os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API key here")

    # Generate the Google Vector embeddings
    embeddings = embeddings_model
    embedded_chunks = embeddings.embed_documents(chunks)
    return embedded_chunks

def create_vector_index(chunks, embedded_chunks, embeddings):
  
    # with open("output.txt", "w") as file:
    #   for item in chunks:
    #       file.write(f"{item}\n")

    text_embedding_pairs = list(zip(chunks, embedded_chunks))

    # Create a document index
    vector_index = FAISS.from_embeddings(text_embedding_pairs, embeddings)
    return vector_index
