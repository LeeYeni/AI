from dotenv import load_dotenv
import os
from chromadb import CloudClient

load_dotenv()

DB_API_KEY = os.getenv("DB_API_KEY")
DB_TENANT = os.getenv("DB_TENANT")
DB_NAME = os.getenv("DB_NAME")

client = CloudClient(
  api_key=DB_API_KEY,
  tenant=DB_TENANT,
  database=DB_NAME
)

# client.delete_collection("vocab_entries")

# --- Chroma 초기화 ---
def get_chroma_collection():

    collection = client.get_or_create_collection(
        name="vocab_entries",
        metadata={
            "hnsw:space": "cosine",
            "description": "English vocabulary embeddings stored by meaning clusters"
        },
        embedding_function=None
    )

    return collection