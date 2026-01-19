from os import getenv
from groq import Groq
from sentence_transformers import SentenceTransformer

groq_client = Groq(api_key=getenv("GROQ_API_KEY"))

embed_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

def embed_texts(texts):
    return embed_model.encode(texts, show_progress_bar=True).tolist()




