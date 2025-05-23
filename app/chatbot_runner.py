# batch_run_questions.py

from chat_utils import query_chromadb, query_llm
from evaluate_metrics import evaluate_answer
from database import SessionLocal, QuestionAnswerLog
from tqdm import tqdm

def load_questions(filepath="questions.txt"):
    with open(filepath, "r") as f:
        return [line.strip() for line in f if line.strip()]

def run_batch():
    session = SessionLocal()
    questions = load_questions("questions.txt")

    for question in tqdm(questions):
        try:
            context = query_chromadb(question)
            answer = query_llm(context)
            score = evaluate_answer(question, answer)

            log_entry = QuestionAnswerLog(
                question=question,
                answer=answer,
                evaluation_score=score
            )
            session.add(log_entry)

        except Exception as e:
            print(f"Error processing question: {question}\n{e}")

    session.commit()
    session.close()
    print("✅ Batch processing complete. All entries saved to database.")

if __name__ == "__main__":
    run_batch()
