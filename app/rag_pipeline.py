from langchain_ollama import OllamaLLM

def generate_answer(question, retrieved_docs):
    llm = OllamaLLM(model="llama3.2:3b")

    context = "\n\n".join(
        f"Source {i + 1} | Page {doc.metadata.get("page_number")}:\n{doc.page_content}"
        for i, doc in enumerate(retrieved_docs)
    )

    prompt = f"""
        You are a helpful document assistant

        Answer the question using only the context below.
        If the answer is not in the context, say: "I don't know based on the provided document."

        Context:
        {context}

        Question:
        {question}

        Answer:
    """

    return llm.invoke(prompt)