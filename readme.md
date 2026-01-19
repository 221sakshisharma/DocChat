# 📄 DocChat – RAG-based Document Chat Application

DocChat is an end-to-end **Retrieval-Augmented Generation (RAG)** application that allows users to upload documents and ask questions about their content. The system retrieves the most relevant document chunks using vector similarity search and generates accurate, context-aware answers using a Large Language Model.

This project demonstrates practical use of **LLMs, vector databases, and backend system design** in a real-world application.

## 🔮 Features

- Source citations in responses
- Multi-document comparison
- Conversation memory
- Document Categorization


## 🧠 RAG Workflow

```
User Query
   ↓
Query Embedding
   ↓
Vector Similarity Search (pgvector)
   ↓
Top-K Relevant Document Chunks
   ↓
Prompt Construction (Query + Context)
   ↓
LLM Generates Final Answer
```

![RAG Architecture](https://media.geeksforgeeks.org/wp-content/uploads/20250210190608027719/How-Rag-works.webp)


## 🛠 Tech Stack & Libraries

### Backend & Database

- **Python**
- **Peewee ORM** – database modeling and queries
- **PostgreSQL (Supabase)** – structured data and embeddings storage
- **pgvector** – vector similarity search
- **psycopg2-binary** – PostgreSQL driver

### AI / ML

- **Embedding Model** – Hugging Face
- **Large Language Model (LLM)** – Groq/OpenAI

### Frontend

- **Streamlit** – interactive web interface


## ⚙️ Setup & Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/docchat.git
cd docchat
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure environment variables

### 4️⃣ Run the application

```bash
streamlit run app.py
```

⭐ **If you find this project useful, consider giving it a star!**
