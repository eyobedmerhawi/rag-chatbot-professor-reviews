import gradio as gr

from retriever import reset_collection, ingest_documents, retrieve
from generator import generate_response


def startup():
    reset_collection()
    ingest_documents()


def ask(question):
    if not question.strip():
        return "", ""

    chunks = retrieve(question)
    result = generate_response(question, chunks)

    answer = result["answer"]
    sources = "\n".join(f"- {source}" for source in result["sources"])

    return answer, sources


with gr.Blocks(title="The Unofficial Guide") as demo:
    gr.Markdown("# The Unofficial Guide")
    gr.Markdown(
        "Ask questions about Georgia State University Computer Science professor reviews."
    )

    question = gr.Textbox(
        label="Question",
        placeholder="Example: What do students say about Data Structures professors?",
    )

    ask_button = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=4)

    ask_button.click(ask, inputs=question, outputs=[answer, sources])
    question.submit(ask, inputs=question, outputs=[answer, sources])

    gr.Examples(
        examples=[
            "What do students say about Data Structures professors?",
            "What do students value most in CS professors?",
            "What makes a CS professor difficult?",
            "What do students say about Machine Learning coursework?",
            "What advice do students give for choosing CS courses?",
        ],
        inputs=question,
    )


if __name__ == "__main__":
    print("Starting The Unofficial Guide...")
    startup()
    demo.launch()