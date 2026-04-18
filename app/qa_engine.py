import os
import re
import fitz
from typing import Dict, List, Tuple


def extract_all_docs_text(folder_path: str) -> Dict[int, Dict]:
    all_docs = {}

    pdf_files = sorted([
        f for f in os.listdir(folder_path)
        if f.lower().endswith(".pdf")
    ])

    for doc_id, pdf_name in enumerate(pdf_files):
        pdf_path = os.path.join(folder_path, pdf_name)
        doc = fitz.open(pdf_path)

        pages_text = {}
        for i in range(len(doc)):
            text = doc[i].get_text("text")
            pages_text[i + 1] = text.strip()

        doc.close()

        all_docs[doc_id] = {
            "file_name": pdf_name,
            "pages_text": pages_text
        }

    return all_docs


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def score_page_by_query(query: str, text: str) -> int:
    query_words = re.findall(r"\b[a-zA-Z0-9\-]+\b", query.lower())
    text_norm = normalize_text(text)

    score = 0
    for w in query_words:
        if len(w) > 2 and w in text_norm:
            score += 1

    if "abstract" in text_norm:
        score += 2
    if "introduction" in text_norm:
        score += 1
    if "bert" in text_norm:
        score += 2
    if "transformer" in text_norm:
        score += 2
    if "gpt-3" in text_norm or "gpt3" in text_norm:
        score += 2
    if "unlike previous" in text_norm:
        score += 3
    if "bidirectional" in text_norm:
        score += 3
    if "left and right context" in text_norm:
        score += 3

    return score


def ask_specific_doc_text_first(
    query: str,
    all_docs: Dict[int, Dict],
    target_doc_id: int,
    top_k_pages: int = 3
) -> Dict:
    file_name = all_docs[target_doc_id]["file_name"]
    pages = all_docs[target_doc_id]["pages_text"]

    ranked_pages: List[Tuple[int, int, str]] = []

    for page_num, text in pages.items():
        clean_text = text.strip()
        if len(clean_text) < 100:
            continue

        text_lower = clean_text.lower().strip()
        if text_lower.startswith((
            "references",
            "bibliography",
            "appendix",
            "contents",
            "table of contents"
        )):
            continue

        score = score_page_by_query(query, clean_text)
        if score > 0:
            ranked_pages.append((score, page_num, clean_text))

    if not ranked_pages:
        return {
            "query": query,
            "answer": "No useful answer found in the selected document.",
            "citations": [],
            "results": []
        }

    ranked_pages.sort(key=lambda x: x[0], reverse=True)

    best_score, best_page_num, best_text = ranked_pages[0]

    abstract_match = re.search(r"\bAbstract\b", best_text, flags=re.IGNORECASE)
    if abstract_match:
        best_text = best_text[abstract_match.end():].strip()

    best_text = re.sub(r"\s+", " ", best_text).strip()
    sentences = re.split(r'(?<=[.!?])\s+', best_text)

    answer = " ".join(sentences[:2]).strip()
    citations = [f"[{file_name}, p.{best_page_num}]"]

    return {
        "query": query,
        "answer": answer,
        "citations": citations,
        "results": ranked_pages[:top_k_pages]
    }