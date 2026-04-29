from document_loader import extract_text_from_pdf, combine_pages, chunk_document

from vector_store import create_vector_store, search_similar_chunks

import streamlit as st

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

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")

    pages = extract_text_from_pdf(uploaded_file)
    full_text = combine_pages(pages)
    chunks = chunk_document(pages)

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

    st.subheader("Search Document")

    question = st.text_input("Ask a question about the document")

    if question: 
        with st.spinner("Searching relevant chunks..."):
            vector_store = create_vector_store(chunks)
            results = search_similar_chunks(vector_store, question)

        st.write("### Most Relevant Chunks")

        for i, (doc, score) in enumerate(results, start=1):
            st.markdown(f"**Result {i}**")
            st.write(f"Page: {doc.metadata.get("page_number")}")
            st.write(f"Similarity Score: {score:.4f}")
            st.text_area(
                f"Chunk {i}",
                value=doc.page_content,
                height=180
            )