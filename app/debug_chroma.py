import os
import chromadb

# Initialize ChromaDB client and collection
client = chromadb.PersistentClient(path=os.path.join(os.path.dirname(__file__), "chroma_db"))
collection = client.get_or_create_collection(name="unh_programs")


def chroma_query(question, top_k=5):
    print(f"[CHROMA] Searching for: {question}")
    results = collection.query(query_texts=[question], n_results=top_k)
    documents = results["documents"][0]
    return documents
