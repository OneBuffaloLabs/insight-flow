from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import tempfile
from src.ingestion import ingest_file
# from src.rag_engine import RAGEngine

# --- Page Config ---
st.set_page_config(
    page_title="Insight Flow | One Buffalo Labs", page_icon="📊", layout="wide"
)

# --- Header ---
st.title("Insight Flow 📊")
st.caption("One Buffalo Labs | RAG-based Analysis Engine")

# --- Sidebar ---
with st.sidebar:
    st.header("Configuration")

    # Check for API Key
    if not os.getenv("OPENAI_API_KEY"):
        st.error("Missing OpenAI API Key in .env file")
        st.stop()

    st.success("API Key Detected")

    # File Uploader
    uploaded_file = st.file_uploader("Upload Data Source", type=("csv"))

    if st.button("Clear Chat History"):
        st.session_state.messages = []

# --- State Management ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Upload a CSV to get started."}
    ]

# --- Logic: Handle File Upload (Phase 2 Focus) ---
if uploaded_file:
    # Save uploaded file to temp path so LangChain can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    try:
        # Ingest data using your new src/ingestion.py
        if (
            "current_file" not in st.session_state
            or st.session_state.current_file != uploaded_file.name
        ):
            with st.spinner("Ingesting data and generating chunks..."):
                docs = ingest_file(tmp_file_path)

                st.session_state.current_file = uploaded_file.name
                st.session_state.docs = docs  # Save docs to state for debugging
                st.success(
                    f"Data Ingested Successfully! Split into {len(docs)} chunks."
                )

        # --- VISUALIZATION (Debugging) ---
        if "docs" in st.session_state:
            with st.expander("🕵️‍♂️ View Ingestion Debugger"):
                st.markdown(
                    f"**Total Documents Created:** `{len(st.session_state.docs)}`"
                )

                # Show the first chunk content
                st.markdown("### First Chunk Preview")
                st.code(st.session_state.docs[0].page_content)

                # Show metadata (source info)
                st.markdown("### Metadata")
                st.json(st.session_state.docs[0].metadata)

    except Exception as e:
        st.error(f"Error during ingestion: {e}")

    finally:
        # Cleanup temp file
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)

# --- Chat Interface ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask a question about your data..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Placeholder Response
    response = "Phase 2 Complete: I have the data chunks ready. (Vector Store implementation coming in Phase 3)"
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
