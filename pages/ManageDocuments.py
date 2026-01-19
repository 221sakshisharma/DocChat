import asyncio
from anyio import sleep
from io import BytesIO

import streamlit as st
from pypdf import PdfReader
from pydantic import BaseModel
from peewee import SQL, JOIN, NodeList

from constants import GET_MATCHING_TAGS_SYSTEM_PROMPT
from db import DocumentInformationChunks, DocumentTags, Tags, db, Documents
from client import groq_client, embed_texts
from utils import Chunk

st.set_page_config(page_title="Manage Documents")
st.title("Manage Documents")

IDEAL_CHUNK_LENGTH = 2000
TAG_PREVIEW_CHUNKS = 5  # limit text sent to LLM


class GeneratedMatchingTags(BaseModel):
    tags: list[str]


async def get_matching_tags(pdf_text: str) -> list[int]:
    existing_tags = list(Tags.select())
    tag_lookup = {tag.name.lower().strip(): tag.id for tag in existing_tags}

    retries = 0
    while True:
        try:
            response = groq_client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {"role": "system", "content": GET_MATCHING_TAGS_SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": (
                            f"Document Text:\n{pdf_text}\n\n"
                            f"Available tags:\n{', '.join(sorted(tag_lookup.keys()))}"
                        ),
                    },
                ],
                temperature=0.2,
            )

            content = response.choices[0].message.content
            ai_tags = GeneratedMatchingTags.model_validate_json(content).tags
            ai_tags = [t.lower().strip() for t in ai_tags]

            matched_ids = [tag_lookup[t] for t in ai_tags if t in tag_lookup]

            if not (2 <= len(matched_ids) <= 3):
                raise ValueError("AI did not return 2–3 valid tags")

            return matched_ids

        except Exception as e:
            retries += 1
            if retries > 5:
                raise
            await sleep(1)


def run_async(coro):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        return asyncio.ensure_future(coro)
    return loop.run_until_complete(coro)


def upload_document(name: str, pdf_file: bytes) -> None:
    reader = PdfReader(BytesIO(pdf_file))
    all_chunks: list[Chunk] = []

    for page_index, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        page_number = page_index + 1

        for i in range(0, len(page_text), IDEAL_CHUNK_LENGTH):
            all_chunks.append({
                "page_index": page_index,
                "chunk_index": i // IDEAL_CHUNK_LENGTH,
                "chunk_content": page_text[i:i + IDEAL_CHUNK_LENGTH],
            })

    preview_text = "\n".join(c["chunk_content"] for c in all_chunks[:TAG_PREVIEW_CHUNKS])
    matching_tag_ids = run_async(get_matching_tags(preview_text))

    with db.atomic():
        document_id = Documents.insert(name=name).execute()
        embeddings = embed_texts([c["chunk_content"] for c in all_chunks])

        DocumentInformationChunks.insert_many([
            {
                "document_id": document_id,
                "chunk_content": c["chunk_content"],
                "embedding": emb,
                "page_index": c["page_index"],
                "chunk_index": c["chunk_index"],
            }
            for c, emb in zip(all_chunks, embeddings)
        ]).execute()

        DocumentTags.insert_many([
            {"document_id": document_id, "tag_id": tag_id}
            for tag_id in matching_tag_ids
        ]).execute()


@st.dialog("Upload document")
def upload_document_dialog():
    pdf_file = st.file_uploader("Upload PDF", type="pdf")

    if pdf_file and st.button("Upload"):
        upload_document(pdf_file.name, pdf_file.read())
        st.rerun()


st.button("Upload Document", on_click=upload_document_dialog)


documents = (
    Documents
    .select(
        Documents.id,
        Documents.name,
        NodeList([
            SQL("array_remove(array_agg("),
            Tags.name,
            SQL("), NULL)")
        ]).alias("tags"),
    )
    .join(DocumentTags, JOIN.LEFT_OUTER)
    .join(Tags, JOIN.LEFT_OUTER)
    .group_by(Documents.id)
    .execute()
)


def delete_document(document_id: int) -> None:
    Documents.delete().where(Documents.id == document_id).execute()


if documents:
    for doc in documents:
        with st.container(border=True):
            st.write(doc.name)
            if doc.tags:
                st.write(f"Tags: {', '.join(doc.tags)}")
            st.button(
                "Delete",
                key=f"delete-{doc.id}",
                on_click=lambda d=doc.id: delete_document(d),
            )
else:
    st.info("No documents created yet.")