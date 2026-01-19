import time
import streamlit as st
from typing import List
from utils import Message, Chunk

from constants import RESPOND_TO_MESSAGE_SYSTEM_PROMPT
from db import DocumentInformationChunks, db, set_diskann_query_rescore
from peewee import SQL
from client import embed_model, groq_client

# ------------------ Streamlit Setup ------------------

st.set_page_config(page_title="Chat With Documents")
st.title("Chat With Documents")


if "messages" not in st.session_state:
    st.session_state["messages"] = []

with st.sidebar:
    if st.button("🗑️ Clear chat"):
        st.session_state["messages"] = []
        st.rerun()


def push_message(message: Message):
    st.session_state["messages"].append(message)

# ------------------ Core Logic ------------------

def send_message(input_message: str):
    # store user message
    push_message({
        "role": "user",
        "content": input_message,
    })

    # embed query
    input_embedding = embed_model.encode([input_message])[0].tolist()

    # retrieve chunks
    related_chunks: List[Chunk] = []

    with db.atomic():
        set_diskann_query_rescore(100)

        results = (
            DocumentInformationChunks
            .select()
            .order_by(SQL("embedding <-> %s::vector", (input_embedding,)))
            .limit(5)
        )

        for row in results:
            related_chunks.append({
                "doc_id": row.document_id,
                "chunk_index": row.chunk_index,
                "chunk_content": row.chunk_content,
                "page_index": row.page_index,
            })

    if not related_chunks:
        push_message({
            "role": "assistant",
            "content": (
                "I can only answer questions using the uploaded documents. "
                "No documents are available right now."
            )
        })
        return

    # build system prompt
    knowledge = "\n".join(
        f"{i + 1}. {chunk['chunk_content']}"
        for i, chunk in enumerate(related_chunks)
    )

    messages = [{
        "role": "system",
        "content": RESPOND_TO_MESSAGE_SYSTEM_PROMPT.replace("{{knowledge}}", knowledge)
    }]

    # add conversation memory (excluding system)
    for msg in st.session_state["messages"]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # retry-safe LLM call
    retries = 0
    while retries < 5:
        try:
            response = groq_client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages,
                temperature=0.3,
            )
            break
        except Exception as e:
            retries += 1
            if retries >= 5:
                raise e
            time.sleep(1)

    assistant_reply = response.choices[0].message.content

    references = [
        f"Document ID: {chunk['doc_id']}, "
        f"Page Index: {chunk['page_index']}, "
        f"Chunk Index: {chunk['chunk_index']}"
        for chunk in related_chunks
    ]

    push_message({
        "role": "assistant",
        "content": assistant_reply,
        "references": references
    })

# ------------------ UI Rendering ------------------

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        refs = message.get("references")
        if refs:
            with st.expander("References"):
                for ref in refs:
                    st.write(ref)

# ------------------ Input ------------------

user_input = st.chat_input("Ask something about the documents...")

if user_input:
    send_message(user_input)
    st.rerun()
