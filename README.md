<h1 align="center">Chat with Document</h1>
<h3 align="center">You're private GPT made for you're documents and pdfs</h1>

<p align="center">
</p>

## Overview

**DocMind AI -** is a secure, private document parsing and retrieval platform designed for organizations like Shera Housing Company and others. It enables C-suite executives and business users to extract, analyze, and query information from internal documents (Excel, PDFs, receipts, etc.) using advanced Large Language Models (LLMs) and embeddings—all without exposing sensitive data to external services.

<div align="center">
  <br>
  <video src="https://github.com/cubixso-dmn-tool/Document-chat-agent/blob/main/Sheera%20-%20Google%20Chrome%202025-06-18%2009-43-15%20(1).mp4?raw=true" width="400" />
  <br>
</div>

## Features

- **Private LLM Integration:** All processing is performed in a secure environment; no document content is sent to external APIs unless explicitly configured.
- **Document Parsing:** Supports Excel files and receipt images for structured and unstructured data extraction.
- **Semantic Search & Retrieval:** Uses state-of-the-art embeddings and vector stores for accurate information retrieval.
- **Interactive Q&A Chatbot:** Natural language interface for querying your documents, with Markdown-formatted responses.
- **Receipt Reader:** Extracts and summarizes key information from uploaded receipts.
- **Role Mapping:** Automatically maps RACI codes to their full forms for clarity in business documents.
- **Extensible:** Modular codebase for easy integration with additional document types or LLM providers.

---

## Demo

![Shera Document GPT Screenshot](white-horizontal.png)

---

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/your-org/document-gpt-shera.git
cd document-gpt-shera
```

### 2. Environment Setup

#### Python Version

- Python 3.10 or higher is recommended.

#### Create a Virtual Environment

```sh
python -m venv venv
venv\Scripts\activate  # On Windows
```

#### Install Requirements

```sh
pip install -r requirements.txt
```

#### Example `requirements.txt`

```
streamlit
pandas
langchain
langchain-community
langchain-core
langchain-openai
langchain-google-genai
scikit-learn
python-dotenv
googletrans==4.0.0-rc1
chromadb
```

---

### 3. Environment Variables

Create a `.env` file in the project root and add your API keys and configuration:

```
OPENAI_API_KEY=your-azure-openai-key
AZURE_OPENAI_ENDPOINT=your-azure-endpoint
GOOGLE_API_KEY=your-google-api-key
```

---

## Usage

### Start the Application

```sh
streamlit run main_1.py
```

### Features

- **File Upload:** Upload Excel files to activate the Q&A chatbot.
- **Receipt Reader:** Upload receipt images (JPG, PNG, PDF) to extract and summarize key information.
- **Product Recommender:** (Coming soon) Get product recommendations based on your receipts.

### Q&A Chatbot

- Ask questions about your uploaded documents in natural language.
- The assistant responds with clear, well-structured Markdown answers, highlighting key information.

---

## Project Structure

```
embeddings.py
file_utils.py
llm_utils.py
main.py
main_1.py
main_2.py
ui_utils.py
white-horizontal.png
```

- `main_1.py`: Streamlit app entry point.
- `embeddings.py`: Embedding initialization and vector store management.
- `file_utils.py`: File validation and Excel processing.
- `llm_utils.py`: LLM-based response generation and reranking.
- `ui_utils.py`: UI customization utilities.
- `white-horizontal.png`: Branding/logo image.

---

## Security & Privacy

- All document processing is performed locally or within your organization's secure environment.
- No document content is sent to external APIs unless explicitly configured.
- Designed for compliance with data privacy regulations.

---

## For Developers

- Modular codebase for easy extension.
- Add new document types or LLM providers by extending the relevant modules.
- Contributions are welcome! Please open issues or pull requests for improvements.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [Streamlit](https://streamlit.io/)
- [scikit-learn](https://scikit-learn.org/)
- [sentence-transformers](https://www.sbert.net/)

---

