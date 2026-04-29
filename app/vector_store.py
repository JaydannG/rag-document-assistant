from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

def create_vector_store(chunks):
    """
    Create an in-memory Chroma vector store from document chunks
    using a free local embedding model.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    documents = [
        Document(
            page_content=chunk["text"],
            metadata=chunk["metadata"]
        )
        for chunk in chunks
    ]

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings
    )

    return vector_store


def search_similar_chunks(vector_store, query, k=4):
    """
    Search for the most relevant chunks for a query.
    """
    return vector_store.similarity_search_with_score(query, k=k)