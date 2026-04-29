from langchain_text_splitters import RecursiveCharacterTextSplitter

from pypdf import PdfReader

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    pages = []

    for page_index, page in enumerate(reader.pages):
        text = page.extract_text() or ""

        pages.append({
            "page_number": page_index + 1,
            "text": text.strip()
        })

    return pages

def combine_pages(pages):
    return "\n\n".join(
        f"Page {page['page_number']}:\n{page["text"]}"
        for page in pages
        if page["text"]
    )

def chunk_document(pages, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = []

    for page in pages:
        page_chunks = splitter.split_text(page["text"])

        for chunk_index, chunk_text in enumerate(page_chunks):
            chunks.append({
                "text": chunk_text,
                "metadata": {
                    "page_number": page["page_number"],
                    "chunk_index": chunk_index
                }
            })

    return chunks