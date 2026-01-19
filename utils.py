from typing import List, Literal, Optional, TypedDict


class Message(TypedDict):
    role: Literal["user", "assistant"]
    content: str
    references: Optional[List[str]]

class Chunk(TypedDict):
    doc_id: Optional[int]
    chunk_index: int
    chunk_content: str
    page_index: int
