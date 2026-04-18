import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import QARequest, QAResponse
from app.qa_engine import extract_all_docs_text, ask_specific_doc_text_first

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")

app = FastAPI(
    title="Multi-Document PDF QA API",
    description="FastAPI backend for grounded question answering over PDF documents",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

all_docs = extract_all_docs_text(DOCS_DIR)

doc_options = {
    doc_info["file_name"]: doc_id
    for doc_id, doc_info in all_docs.items()
}


@app.get("/")
def root():
    return {
        "message": "FastAPI PDF QA backend is running",
        "available_docs": list(doc_options.keys())
    }


@app.get("/documents")
def list_documents():
    return {
        "documents": [
            {"doc_id": doc_id, "file_name": file_name}
            for file_name, doc_id in doc_options.items()
        ]
    }


@app.post("/ask", response_model=QAResponse)
def ask_question(payload: QARequest):
    if payload.selected_doc not in doc_options:
        raise HTTPException(status_code=404, detail="Selected document not found.")

    doc_id = doc_options[payload.selected_doc]

    response = ask_specific_doc_text_first(
        query=payload.query,
        all_docs=all_docs,
        target_doc_id=doc_id,
        top_k_pages=3
    )

    top_pages = []
    for score, page_num, _ in response["results"]:
        top_pages.append(f"{payload.selected_doc} | page={page_num} | text_score={score}")

    return QAResponse(
        query=payload.query,
        selected_doc=payload.selected_doc,
        answer=response["answer"],
        citations=response["citations"],
        top_pages=top_pages
    )