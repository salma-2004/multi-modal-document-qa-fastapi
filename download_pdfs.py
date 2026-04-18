import os
import requests

os.makedirs("docs", exist_ok=True)

pdf_urls = {
    "doc_1.pdf": "https://arxiv.org/pdf/1706.03762.pdf",
    "doc_2.pdf": "https://arxiv.org/pdf/1810.04805.pdf",
    "doc_3.pdf": "https://arxiv.org/pdf/2005.14165.pdf"
}

for filename, url in pdf_urls.items():
    print(f"Downloading {filename} ...")
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    file_path = os.path.join("docs", filename)
    with open(file_path, "wb") as f:
        f.write(response.content)

    print(f"Saved: {file_path}")

print("\nDone. Files inside docs:")
for file_name in os.listdir("docs"):
    print("-", file_name)