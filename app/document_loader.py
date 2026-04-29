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