# app/utils.py

import os
import time
from typing import List, Callable, Any
from functools import wraps

def retry_on_failure(max_retries: int = 3, delay: int = 2):
    """
    Decorator to retry a function up to `max_retries` times if it raises an exception,
    waiting `delay` seconds between attempts.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exc = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    print(f"[retry_on_failure] Attempt {attempt}/{max_retries} failed: {e}")
                    time.sleep(delay)
            print(f"[retry_on_failure] All {max_retries} retries failed.")
            raise last_exc
        return wrapper
    return decorator

def truncate_context(docs: List[str], max_words: int = 600) -> str:
    """
    Combine a list of text chunks and truncate to at most `max_words` words.
    """
    combined = " ".join(docs)
    words = combined.split()
    return " ".join(words[:max_words])

def load_questions(file_path: str) -> List[str]:
    """
    Read a text file of questions (one per non-empty line) and return as a list.
    """
    questions: List[str] = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            q = line.strip()
            if q:
                questions.append(q)
    return questions

# RAG glue: get relevant chunks + query Ollama
from debug_chroma import chroma_query as get_relevant_chunks
from embed_documents import query_ollama

@retry_on_failure(max_retries=3, delay=2)
def query_chroma_and_ollama(question: str, model_name: str) -> str:
    """
    1) Retrieve top chunks for the question via ChromaDB.
    2) Truncate/assemble context.
    3) Query Ollama with the context and return the answer.
    """
    chunks = get_relevant_chunks(question)
    context = truncate_context(chunks)
    answer = query_ollama(question, context, model_name=model_name)
    return answer
