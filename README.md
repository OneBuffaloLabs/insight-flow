# Insight Flow 🧠

> **RAG-based analysis engine allowing natural language querying of CSV and SQLite datasets.**

![CI Status](https://github.com/OneBuffaloLabs/insight-flow/actions/workflows/ci.yml/badge.svg)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)

## 📖 About

**Insight Flow** is an interactive analysis engine designed to bridge the gap between structured data and natural language. It utilizes **Retrieval-Augmented Generation (RAG)** to allow users to chat with their data.

Built for **One Buffalo Labs**, this project demonstrates how to ingest CSV or SQLite data, chunk it into vector embeddings using **ChromaDB**, and retrieve context-aware answers using **LangChain** and **OpenAI**.

## 🛠 Tech Stack

- **Runtime:** Python 3.10 - 3.12
- **Frontend:** Streamlit
- **Orchestration:** LangChain
- **Vector Store:** ChromaDB (Local persistent storage)
- **LLM:** OpenAI (GPT-3.5-Turbo / GPT-4)
- **Linting:** Ruff

## 🚀 Getting Started

This project includes a `Makefile` to automate environment setup.

### ⚠️ System Prerequisites (Crucial)

Because this project uses **ChromaDB**, you must have C++ build tools installed to compile the vector engine extensions.

**Ubuntu / Debian:**

```bash
sudo apt-get update
sudo apt-get install python3-dev build-essential
```

**MacOS:**

```bash
xcode-select --install
```

### Quick Start

1. **Clone the repository**

```bash
git clone [https://github.com/OneBuffaloLabs/insight-flow.git](https://github.com/OneBuffaloLabs/insight-flow.git)
cd insight-flow

```

2. **Configure Environment**
   Create a `.env` file in the root directory and add your OpenAI API Key:

```bash
OPENAI_API_KEY=sk-your-key-here

```

3. **Install Dependencies**
   This command builds the virtual environment and compiles necessary extensions.

```bash
make install

```

4. **Run the Application**
   Launches the Streamlit server on port 3000.

```bash
make run

```

## ⚡ Features & Usage

1. **Data Ingestion:** Automatically loads CSV files from the `data/` directory or connects to SQLite databases. 2. **Vector Embedding:** Converts text data into high-dimensional vectors for semantic search. 3. **Context Retrieval:** Finds the most relevant data rows based on your natural language query. 4. **Generative Response:** Synthesizes the retrieved data into a clear, human-readable answer.

## ⚙️ Developer Command Reference

We use `make` to abstract common development tasks.

| Command        | Description                                                  |
| -------------- | ------------------------------------------------------------ |
| `make install` | Create venv, upgrade pip, and install dependencies.          |
| `make run`     | Run the Streamlit application (Localhost:3000).              |
| `make clean`   | Nuke virtual environment and compiled bytecode (Hard Reset). |
| `make lint`    | Run `ruff` to identify code quality issues.                  |
| `make format`  | Auto-format code using `ruff`.                               |
| `make fix`     | Auto-fix linting errors.                                     |

##📂 Project Structure

```text
/
├── app.py # Main application entry point (UI)
├── src/
│ └── rag_engine.py # RAG logic, Vector setup, and QA Chains
├── data/ # Place CSV/SQLite files here
├── requirements.txt # Pinned dependencies
├── Makefile # Automation commands
└── .env # API Keys (Not committed)
```

## 🧪 Quality Control

We enforce code quality standards using **Ruff**.

```bash
# Check for errors
make lint

# Auto-format code
make format
```

---

_Built by **Andrew Elbaneh** for [One Buffalo Labs](https://onebuffalolabs.com)._

**License**
[MIT](https://www.google.com/search?q=LICENSE) - Copyright (c) 2025 One Buffalo Labs
