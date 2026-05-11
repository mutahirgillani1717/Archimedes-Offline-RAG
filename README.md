# ΛRCHIMEDES // Offline Document Intelligence

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-FFFFFF?style=for-the-badge&logo=ollama&logoColor=black)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F00?style=for-the-badge&logo=database&logoColor=white)

A 100% offline, privacy-first Retrieval-Augmented Generation (RAG) desktop application. Archimedes allows users to query complex technical documents using natural language without sending sensitive proprietary data to the cloud. Designed with a custom "Industrial Noir" UI and engineered for Edge AI hardware.
<img width="960" height="504" alt="image" src="https://github.com/user-attachments/assets/860da1df-4c48-4a77-8138-c71bede8fbe5" />


## 🧠 System Architecture

* **LLM Engine:** Local Llama 3.2 (3B parameters) served via Ollama.
* **Vector Database:** ChromaDB for high-speed semantic similarity search.
* **Embeddings:** HuggingFace `all-MiniLM-L6-v2` for efficient document vectorization.
* **UI/UX:** CustomTkinter with a threaded, event-driven architecture.

## ⚡ Key Engineering Features

* **Zero Cloud Dependency:** Completely air-gapped inference. Ideal for proprietary corporate data, legal documents, or sensitive system blueprints.
* **Contextual Retrieval Tuning:** Implemented optimized Recursive Character Splitting (1000 char chunks, 200 overlap) and `k=5` retrieval to maintain complex mathematical equations and architectural context without losing data continuity.
* **Threaded Processing:** Decoupled the UI from the AI inference engine using Python's `threading` module, preventing UI freezing and application crashes during heavy vector retrieval.
* **Dynamic Asset Generation:** The application programmatically generates its own geometric `.ico` branding assets on the first run via `Pillow` (PIL), ensuring the repository remains lightweight and dependency-free.

## 🛠️ Installation & Usage

### 1. Prerequisites
Ensure you have Python 3.9+ installed and [Ollama](https://ollama.com/) running on your system.
Pull the local LLM brain:
```bash
ollama run llama3.2:3b
