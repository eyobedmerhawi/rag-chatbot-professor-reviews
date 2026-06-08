from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL


_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded response using only retrieved chunks.
    """

    if not retrieved_chunks:
        return {
            "answer": "I don't have enough information in the documents to answer that.",
            "sources": [],
        }

    context = "\n\n".join(
        f"[Source: {chunk['source']} | Distance: {chunk['distance']:.3f}]\n{chunk['text']}"
        for chunk in retrieved_chunks
    )

    sources = sorted(set(chunk["source"] for chunk in retrieved_chunks))

    system_prompt = """
You are an assistant for The Unofficial Guide.

Answer the user's question using ONLY the provided retrieved context.
Do not use outside knowledge.
Do not guess or invent details.
If the context does not contain enough information, say:
"I don't have enough information in the documents to answer that."

Every answer must mention the source document names that support it.
Keep the answer clear, concise, and grounded in the retrieved student-generated documents.
"""

    user_prompt = f"""
Retrieved context:
{context}

User question:
{query}
"""

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": sources,
    }


if __name__ == "__main__":
    from retriever import retrieve

    query = "What do students say about Data Structures professors?"
    chunks = retrieve(query)
    result = generate_response(query, chunks)

    print("Answer:")
    print(result["answer"])

    print("\nSources:")
    for source in result["sources"]:
        print(f"- {source}")
