import os
from config import DOCUMENTS_PATH


def load_documents():
    """
    Load all .txt files from the documents folder.
    """

    documents = []

    for filename in os.listdir(DOCUMENTS_PATH):
        if filename.endswith(".txt"):
            filepath = os.path.join(DOCUMENTS_PATH, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            documents.append(
                {
                    "source": filename,
                    "text": text,
                }
            )

    return documents


def chunk_text(text, chunk_size=300, overlap=50):
    """
    Split text into overlapping chunks.
    """

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)

    return chunks


def create_chunks(documents):
    """
    Convert documents into chunk records.
    """

    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append(
                {
                    "text": chunk,
                    "source": doc["source"],
                    "chunk_id": f"{doc['source']}_{i}",
                }
            )

    return all_chunks


if __name__ == "__main__":
    docs = load_documents()
    chunks = create_chunks(docs)

    print(f"Loaded {len(docs)} documents")
    print(f"Created {len(chunks)} chunks")

    for chunk in chunks[:5]:
        print("\n---")
        print(chunk["source"])
        print(chunk["text"][:200])