import streamlit as st
import os
import tempfile
from src.rag_engine import RAGEngine

# --- Page Config ---
st.set_page_config(
    page_title="Insight Flow | One Buffalo Labs",
    page_icon="📊",
    layout="wide"
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
    st.session_state.messages = [{"role": "assistant", "content": "Upload a CSV to get started."}]

if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = RAGEngine()

# --- Logic: Handle File Upload ---
if uploaded_file:
    # Save uploaded file to temp path so LangChain can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    # Ingest data (Only if new file)
    if "current_file" not in st.session_state or st.session_state.current_file != uploaded_file.name:
        with st.spinner("Ingesting data and generating embeddings..."):
            st.session_state.rag_engine.ingest_file(tmp_file_path)
            st.session_state.current_file = uploaded_file.name
            st.success("Data Ingested Successfully!")

# --- Chat Interface ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask a question about your data..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Placeholder Response
    response = "I received your message! (Logic coming in next step)"
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)