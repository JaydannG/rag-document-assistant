import streamlit as st
from document_loader import extract_text_from_pdf, combine_pages

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

    st.subheader("Document Info")
    st.write(f"**Pages:** {len(pages)}")
    st.write(f"**Characters Extracted:** {len(full_text):,}")

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

