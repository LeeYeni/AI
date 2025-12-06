from vector_db.chroma_client import get_chroma_collection
from vector_db.store import store

collection = get_chroma_collection()
print("collection BEFORE store:", type(collection))

def vocab_ingest_pipeline(embedded_dataset: list):
    store(embedded_dataset, collection)