# app/chatbot_api.py

import os, time
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import reset_table, log_qa_interaction
from debug_chroma import chroma_query
from embed_documents import query_ollama
from utils import truncate_context
from evaluate_metrics import get_bleu_score, get_rouge_score

app = FastAPI()

# Reset logs table once at startup
@app.on_event("startup")
async def on_startup():
    reset_table()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask(
    question: str = Form(...),
    model_name: str = Form(None)
):
    start = time.time()
    model = model_name or os.getenv("MODEL_NAME", "mistral")

    # 1) Fetch & truncate context
    try:
        docs    = chroma_query(question)
        context = truncate_context(docs)
    except Exception as e:
        context = None
        print(f"[chatbot_api] Context fetch failed: {e}")

    # 2) Get answer
    try:
        answer = query_ollama(question, context, model)
    except Exception as e:
        return JSONResponse({"error": f"RAG pipeline failed: {e}"}, status_code=500)

    response_time = round(time.time() - start, 4)

    # 3) Compute metrics
    try:
        bleu  = get_bleu_score(question, answer)
        rouge = get_rouge_score(question, answer)
        eval_score = round((bleu + rouge) / 2, 4)
    except Exception as e:
        print(f"[chatbot_api] Metric error: {e}")
        bleu = rouge = eval_score = None

    # 4) (Optional) confidence placeholder
    confidence = None

    # 5) Log to DB
    try:
        log_qa_interaction(
            question=question,
            answer=answer,
            response_time=response_time,
            evaluation_score=eval_score,
            context=context,
            confidence_score=confidence,
            bleu_score=bleu,
            rouge_score=rouge
        )
    except Exception as e:
        print(f"[chatbot_api] Logging failed: {e}")

    # 6) Return full JSON
    return JSONResponse({
        "answer": answer,
        "response_time": response_time,
        "evaluation_score": eval_score,
        "bleu_score": bleu,
        "rouge_score": rouge,
        "context": context
    })
