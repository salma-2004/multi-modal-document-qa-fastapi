from pydantic import BaseModel
from typing import List


class QARequest(BaseModel):
    query: str
    selected_doc: str


class QAResponse(BaseModel):
    query: str
    selected_doc: str
    answer: str
    citations: List[str]
    top_pages: List[str]