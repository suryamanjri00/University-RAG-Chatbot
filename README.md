# 🧠 UNH RAG Chatbot – AI Assistant for University of New Haven

This is a production-grade, GPU-accelerated Retrieval-Augmented Generation (RAG) chatbot that answers queries about the University of New Haven using scraped web data. It uses **ChromaDB**, **Ollama LLM**, and **Apache Airflow** for automation, with deployment on **AWS EC2 (GPU)**.

---

## 🚀 Features

- 🔍 Scrapes university content using sitemap filtering  
- 🧠 Embeds documents into ChromaDB with `all-MiniLM-L6-v2`  
- 💬 **Interactive Chat Interface** – Simple and user-friendly web-based chatbot  
- 🔍 **Vector Search** with ChromaDB – Efficient information retrieval  
- 💬 Uses **Ollama Mistral 7B (LLM)** for fast, high-quality answers  
- 🧩 Chunked input for semantic search (`chunk size = 500`, `overlap = 100`)  
- ⚙️ Airflow DAG automates monthly refresh of documents  
- 🎛️ Configurable via `config.yaml` (no code changes needed)  
- 🔴 Real-time Updates – Continuously learns from new data  
- ☁️ Deployment Ready – Can be hosted on cloud platforms  

---

## 🧠 Tech Stack

- **LLM**: Ollama Mistral 7B  
- **Embeddings**: Hugging Face `all-MiniLM-L6-v2`  
- **Vector Store**: ChromaDB  
- **Web API**: FastAPI  
- **Scheduler**: Apache Airflow  
- **Deployment**: AWS EC2 (GPU)  
- **Frontend**: HTML/CSS/JS + Bootstrap  

---

## 📡 Pipeline Summary

### 🔄 Data Flow:

**Scraping**  
- Uses sitemap: `https://university.edu/sitemap.xml`  
- Filters: admissions, international, tuition, programs, student life  
- Excludes: blogs, newsletters, events  

**Cleaning**  
- Removes HTML noise → stores in `cleaned_texts/`  

**Embedding**  
- Chunks text (`size=500`, `overlap=100`)  
- Embeds via `SentenceTransformers` → stores in ChromaDB  

### 💬 Chatbot Flow:

1. User submits query via FastAPI  
2. Retrieves relevant chunks from ChromaDB  
3. Passes context + query to **Ollama Mistral 7B**  
4. Returns an answer in under 5 seconds  

### ⏱️ Airflow Automation:

- DAG scheduled for 1st of every month to:  
  - Re-scrape site  
  - Clean + re-embed documents  
  - Use `config.yaml` parameters (model, chunk size, sitemap)

---

## ⚙️ Setup Instructions

1. **Clone the Repo**
```bash
git clone https://github.com/jureddy9706/UNH_CHATBOT.git
cd UNH_CHATBOT
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Update Config (Optional)**  
Edit `config.yaml`:
```yaml
model_name: "mistral"
embedding_model: "all-MiniLM-L6-v2"
chunk_size: 500
overlap: 100
sitemap_url: "https://university.edu/sitemap.xml"
```

4. **Run Chatbot Locally**
```bash
uvicorn app.chatbot_api:app --reload
```

5. **Launch Airflow in a Separate Terminal**
```bash
airflow standalone
```

---

## 🧪 Example Chatbot Demo

```text
User: Who is Sula?
Bot: Ardiana Sula is a recognized scholar and researcher...

User: Who is Aminul?
Bot: Muhammad Aminul Islam is an Assistant Professor...

User: Vahis?
Bot: Based on the context, 'vahis' is not mentioned...

User: Vahid?
Bot: Vahid Behzadan is an assistant professor...
```

---

## ☁️ EC2 Deployment (Optional)

1. Launch Ubuntu GPU EC2  
2. SSH into instance  
3. Install Python 3.10+, Ollama, system packages  
4. Clone repo, install dependencies  
5. Start chatbot:
```bash
uvicorn app.chatbot_api:app --host 0.0.0.0 --port 8000
```
Access from browser: `http://<EC2-IP>:8000`

---

## 🔧 Customization

To build a chatbot for another college, just change the **sitemap URL** and update `config.yaml` or Airflow.  
➡️ **No code changes required!**
