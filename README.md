# Multi-Modal Document QA using FastAPI

This project implements a **multi-document Question Answering (QA) system** over PDF files.  
It returns **grounded answers with page-level citations** using text extraction and lightweight reranking.

---

## Features

- Multi-document PDF support  
- Text extraction using **PyMuPDF**  
- Query-based page ranking  
- Citation-based answers  
- FastAPI backend  
- Interactive API testing with Swagger UI  

---

## Project Structure

```bash
fastapi_pdf_qa/
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
```

---

## How It Works

The system follows this pipeline:

1. User sends a query
2. User selects a document
3. PDF text is searched page by page
4. Pages are ranked based on query relevance
5. The best page is selected
6. The answer is generated with citation

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/salma-2004/multi-modal-document-qa-fastapi.git
cd multi-modal-document-qa-fastapi
```

### 2. Create and activate virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\Activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Download PDFs

If the PDFs are not already inside `docs/`, run:

```bash
python download_pdfs.py
```

---

## Run the API

```bash
uvicorn app.main:app --reload
```

Then open:

* Root: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## API Endpoints

### `GET /`

Check server status

### `GET /documents`

List available PDF documents

### `POST /ask`

Submit a query and get:

* answer
* citations
* top ranked pages

---

## Example Request

```json
{
  "query": "How does BERT differ from previous language models?",
  "selected_doc": "doc_2.pdf"
}
```

---

## Example Response

```json
{
  "query": "How does BERT differ from previous language models?",
  "selected_doc": "doc_2.pdf",
  "answer": "BERT is designed to pre-train deep bidirectional representations by conditioning on both left and right context in all layers.",
  "citations": [
    "[doc_2.pdf, p.1]"
  ],
  "top_pages": [
    "doc_2.pdf | page=1 | text_score=19",
    "doc_2.pdf | page=8 | text_score=18",
    "doc_2.pdf | page=2 | text_score=17"
  ]
}
```

---

## Evaluation

The system was tested on three research papers:

* Transformer
* BERT
* GPT-3

### Sample Questions

* What is the main contribution of the Transformer paper?
* How does BERT differ from previous language models?
* What is the main idea of GPT-3?

---

## Author

**Salma Khairy**
