# 📄 Local RAG Document Assistant

A retrieval-augmented generation (RAG) system that allows users to upload PDF documents and ask questions, with answers grounded in the document and supported by source citations

---

## Overview

This project implements an end-to-end **Rag Pipeline** using local models.
It enables users to query documents and receive context-aware answers generated from relevant sections of the text.

The system avoids hallucinations by restricting responses to retrieved document content and explicitly returns *"I don't know"* when information is not available.

---

## Features

- Upload and process PDF documents
- Automatic text extraction and chunking]
- Local embeddings using `sentence-transformers`
- Vector search using `ChromaDB`
- Local LLM inference via `Ollama`
- Source-grounded answers with citations
- Adjustable chunking and retrieval parameters
- Chat history support
- Evaluation pipeline for retrieval and answer quality

---

## How it works

1. **Document Ingestion**
    - Extract text from uploaded PDFs using `pypdf`

2. **Chunking**
    - Split text into overlapping chunks using recursive splitting

3. **Embedding**
    - Convert chunks into vector embeddings using `all-MiniLM-L6-v2`

4. **Retrieval**
    - Use similarity search (ChromaDB) to find relevant chunks

5. **Generation**
    - Pass retrieved context to a local LLM (Ollama)
    - Generate answers constrained to the retrieved content

6. **Citation**
    - Display source pages and chunks used to generate the answer

---

## Tech Stack

- **Frontend:** Streamlit  
- **Embeddings:** sentence-transformers (`all-MiniLM-L6-v2`)  
- **Vector DB:** ChromaDB  
- **LLM:** Ollama (`llama3.2:3b`)  
- **Frameworks:** LangChain  
- **Language:** Python  

--- 

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/rag-document-assistant.git
cd rag-document-assistant
```

### Create virtual environment:

```
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies:

```
pip install -r requirements.txt
```

### Install and start Ollama:

```
sudo systemctl enable --now ollama
ollama pull llama3.2:3b
```

## Usage

### Run the app:

```
streamlit run app/streamlit_app.py
```

Then:
1. Upload a PDF
2. Ask a question
3. View answer + supporting sources

## Evaluation

The system was evaluated using a fixed set of question-answer pairs over a sample document.

### **Metrics**
* Retrieval Accuracy: 75%
* Grounded Answer Rate: 100%
* Failure Cases:
    * Ambiguous queries
    * Missing document information

The model correctly return *"I don't know* for queries outside of the document, demonstrating controlled hallucination behavior

## Future Improvements

* Support for multiple documents
* Support for multiple documents
* Persistent vector storage
* Better ranking (reranking models)
* Streaming responses
* OCR support for scanned PDFs
* UI improvements