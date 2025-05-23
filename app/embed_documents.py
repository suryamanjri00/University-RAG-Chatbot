import os
from sentence_transformers import SentenceTransformer
import chromadb
from langchain_ollama import OllamaLLM

# ──────────────────────────────────────────────
# Initialize ChromaDB Client
db_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
client = chromadb.PersistentClient(path=db_dir)
collection = client.get_collection(name="unh_programs")

# ──────────────────────────────────────────────
# Load Embedding Model (same as during indexing)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ──────────────────────────────────────────────
def retrieve_context(question: str, top_k: int = 5) -> str:
    """
    Retrieve top-k most relevant context chunks from ChromaDB.
    """
    question_embedding = embedding_model.encode(question).tolist()
    
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
        include=["documents"]
    )
    
    documents = results.get("documents", [[]])[0]
    if not documents:
        return ""  # No relevant chunks found
    return "\n".join(documents)

# ──────────────────────────────────────────────
def query_ollama(question: str, context: str, model_name: str = "mistral") -> str:
    """
    Send the question + retrieved context to Ollama and get the answer.
    """
    llm = OllamaLLM(model=model_name)
    
    prompt = (
        "You are a helpful assistant. Answer the user's question based ONLY on the following context.\n"
        "If the answer is not contained within the context, reply: 'I don't know based on the provided context.'\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n"
        "Answer:"
    )
    
    return llm(prompt)

# ──────────────────────────────────────────────
def rag_pipeline(question: str, model_name: str = "mistral") -> str:
    """
    Full RAG pipeline: retrieve context → send to LLM → get answer.
    """
    context = retrieve_context(question)
    if not context.strip():
        return "I don't know based on the provided context."  # No context found
    
    answer = query_ollama(question, context, model_name=model_name)
    return answer

# ──────────────────────────────────────────────
if __name__ == "__main__":
    while True:
        user_question = input("\nAsk me a question (or type 'exit'): ")
        if user_question.lower() == "exit":
            break
        
        answer = rag_pipeline(user_question, model_name="mistral")
        print("\nAnswer:", answer)
