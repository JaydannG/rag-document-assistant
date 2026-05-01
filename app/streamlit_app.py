from document_loader import extract_text_from_pdf, combine_pages, chunk_document

from vector_store import create_vector_store, search_similar_chunks

from rag_pipeline import generate_answer

import streamlit as st

@st.cache_resource
def get_vector_store(_chunks):
    return create_vector_store(_chunks)

st.set_page_config(
    page_title="RAG Document Assistant",
    layout="wide"
)

st.title("📄 RAG Document Assistant")
st.write("Upload a PDF and extract its text")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

st.sidebar.header("Settings")

chunk_size = st.sidebar.slider("Chunk Size", 500, 2000, 1000, 100)
chunk_overlap = st.sidebar.slider("Chunk Overlap", 0, 500, 200, 50)
top_k = st.sidebar.slider("Retrived Chunks", 1, 8, 4)

if "messages" not in st.session_state:
    st.session_state.messages = []

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")

    pages = extract_text_from_pdf(uploaded_file)
    full_text = combine_pages(pages)
    chunks = chunk_document(
        pages,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    st.subheader("Document Info")
    st.write(f"**Pages:** {len(pages)}")
    st.write(f"**Characters Extracted:** {len(full_text):,}")
    st.write(f"**Chunks Created:** {len(chunks)}")

    st.subheader("Text Preview")

    preview_length = 3000

    if full_text.strip():
        st.text_area(
            "Extracted Text",
            value=full_text[:preview_length],
            height=400
        )

        if len(full_text) > preview_length:
            st.info(f"Showing first {preview_length} characters only")
    else:
        st.warning("No text could be extracted from this PDF.")

    st.subheader("Chunk Preview")

    if chunks:
        selected_chunk = st.selectbox(
            "Choose a chunk",
            range(len(chunks)),
            format_func=lambda i: f"Chunk {i + 1} - Page {chunks[i]["metadata"]["page_number"]}"
        )

        st.text_area(
            "Chunk Text",
            value=chunks[selected_chunk]["text"],
            height=250
        )

    st.subheader("Ask a Question")

    question = st.text_input("Ask a question about the document")

    if question:
        with st.spinner("Searching relevant chunks..."):
            vector_store = get_vector_store(chunks)
            results = search_similar_chunks(vector_store, question, k=top_k)

        retrieved_docs = [doc for doc, score in results]

        with st.spinner("Generating answer..."):
            answer = generate_answer(question, retrieved_docs)

        st.write("### Answer")
        st.write(answer)

        st.session_state.messages.append({
            "question": question,
            "answer": answer
        })

        st.write("### Sources")

        for i, (doc, score) in enumerate(results, start=1):
            with st.expander(f"Source {i} — Page {doc.metadata.get("page_number")}, Chunk {doc.metadata.get("chunk_index")}"):
                st.write(f"Similarity score: {score:.4f}")
                st.write(doc.page_content)

    st.subheader("Chat History")

    for message in reversed(st.session_state.messages):
        with st.expander(message["question"]):
            st.write(message["answer"])