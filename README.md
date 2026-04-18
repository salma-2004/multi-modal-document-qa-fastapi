# Multi-Modal Document QA using ColPali and FastAPI

This project implements a multi-document Question Answering (QA) system over PDF files.  
It combines **multi-modal retrieval** and **text-based reranking** to return grounded answers with page-level citations.

## Features

- Multi-document support
- PDF text extraction using **PyMuPDF**
- Hybrid retrieval and reranking pipeline
- Grounded answers with citations
- FastAPI backend
- Interactive API testing via Swagger UI

## Project Structure

```bash
multi-modal-document-qa-fastapi/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── qa_engine.py
│   └── schemas.py
│
├── docs/
│   ├── doc_1.pdf
│   ├── doc_2.pdf
│   └── doc_3.pdf
│
├── download_pdfs.py
├── requirements.txt
├── README.md
└── .gitignore