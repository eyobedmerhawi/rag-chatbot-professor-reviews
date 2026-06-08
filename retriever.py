import chromadb
from chromadb.utils import embedding_functions

from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL, N_RESULTS
from ingest import load_documents, create_chunks


_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)

_client = chromadb.PersistentClient(path=CHROMA_PATH)

_collection = _client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=_ef,
    metadata={"hnsw:space": "cosine"},
)


def reset_collection():
    """
    Clear existing vector store collection.
    """
    global _collection

    try:
        _client.delete_collection(CHROMA_COLLECTION)
    except Exception:
        pass

    _collection = _client.get_or_create_collection(
        name=CHROMA_COLLECTION,
        embedding_function=_ef,
        metadata={"hnsw:space": "cosine"},
    )


def ingest_documents():
    """
    Load documents, chunk them, and store chunks in ChromaDB.
    """
    documents = load_documents()
    chunks = create_chunks(documents)

    if not chunks:
        print("No chunks found.")
        return

    _collection.add(
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[{"source": chunk["source"]} for chunk in chunks],
        ids=[chunk["chunk_id"] for chunk in chunks],
    )

    print(f"Loaded {len(documents)} documents")
    print(f"Stored {len(chunks)} chunks in ChromaDB")


def retrieve(query, n_results=N_RESULTS):
    """
    Retrieve top relevant chunks for a query.
    """
    if _collection.count() == 0:
        return []

    results = _collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    chunks = []

    for text, metadata, distance in zip(documents, metadatas, distances):
        chunks.append(
            {
                "text": text,
                "source": metadata.get("source", "Unknown"),
                "distance": distance,
            }
        )

    return chunks


if __name__ == "__main__":
    reset_collection()
    ingest_documents()

    test_query = "What do students say about Data Structures professors?"
    results = retrieve(test_query)

    print(f"\nQuery: {test_query}")

    for result in results:
        print("\n---")
        print(f"Source: {result['source']}")
        print(f"Distance: {result['distance']:.3f}")
        print(result["text"][:300])
