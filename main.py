import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="DocChat", layout="wide")

st.markdown("""
# 📄 DocChat – RAG-based Document Chat Application

DocChat is an end-to-end **Retrieval-Augmented Generation (RAG)** application that allows users to upload documents and ask questions about their content. The system retrieves the most relevant document chunks using vector similarity search and generates accurate, context-aware answers using a Large Language Model.

This project demonstrates practical use of **LLMs, vector databases, and backend system design** in a real-world application.

## 🔮 Features

- Source citations in responses
- Multi-document comparison
- Conversation memory
- Document Categorization
""")