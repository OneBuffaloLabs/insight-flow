# Insight Flow 📊

> **A "Chat with your Data" engine emphasizing transparency and strict sourcing.**

![CI Status](https://github.com/OneBuffaloLabs/insight-flow/actions/workflows/ci.yml/badge.svg)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain.com)

## 📖 The "Why"

I built **Insight Flow** to solve a specific problem: trusting LLM analysis. Standard chatbots often hallucinate when analyzing private data. This engine is designed to be a **strict analyst**.

It uses a RAG (Retrieval-Augmented Generation) pipeline to ingest local CSVs, but with a twist: **it forces transparency**. Every answer includes a "Source Dropdown" showing the exact raw data rows the model used. If the data isn't there, the system prompt forces it to say "I don't know" rather than guessing.

**Core Tech:** Python 3.12, Streamlit, LangChain, ChromaDB (Vectors), OpenAI.

## 🚀 Quick Start

This repo uses a `Makefile` to handle the messy Python venv setup and execution.

### 1. Prerequisites (Don't skip this)

ChromaDB requires C++ compilers for its vector indexing. If you get a `chroma-hnswlib` error during install, you likely need this:

- **Ubuntu/Debian:** `sudo apt-get install python3-dev build-essential`
- **MacOS:** `xcode-select --install`

### 2. Install & Run

```bash
# Clone & Enter
git clone [https://github.com/OneBuffaloLabs/insight-flow.git](https://github.com/OneBuffaloLabs/insight-flow.git)
cd insight-flow

# Setup Env (Needs your API Key)
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# Auto-install (creates venv, installs dependencies)
make install

# Launch UI (Localhost:3000)
make run

```

## ⚡ What makes this different?

Most RAG tutorials just dump text into a database. Insight Flow adds a "Senior Analyst" layer:

- **Transparency First:** The UI renders the raw source documents in an expander for every single answer. You can verify the math yourself.
- **Anti-Hallucination:** The system prompt is tuned to reject questions outside the dataset's scope.
- **Analyst Controls:** A sidebar slider adjusts the "Temperature." Keep it at `0.0` for strict data reporting, or bump it up if you want the model to brainstorm trends.

## 📂 Project Structure

- `app.py`: The frontend. Handles the Streamlit session state, file uploads, and chat bubbles.
- `src/rag_engine.py`: The brain. Manages the ChromaDB vector store, embedding generation, and LangChain retrieval logic.
- `Makefile`: Shortcuts for dev workflows (`make clean`, `make lint`, etc).
- `requirements.txt`: Pinned production dependencies.

---

_Built by **Andrew Elbaneh** @ [One Buffalo Labs](https://onebuffalolabs.com)._
**License** [MIT](https://www.google.com/search?q=LICENSE)
