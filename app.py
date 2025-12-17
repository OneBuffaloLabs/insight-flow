import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from src.rag_engine import RAGEngine

load_dotenv()

# --- Page Config ---
st.set_page_config(
    page_title="Insight Flow | One Buffalo Labs", page_icon="📊", layout="wide"
)

# --- Header ---
st.title("Insight Flow 📊")
st.caption("One Buffalo Labs | RAG-based Analysis Engine")

# --- State Management ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Upload a CSV to get started."}
    ]

# Initialize the RAG Engine once and persist it in session state
if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = RAGEngine()

# --- Sidebar ---
with st.sidebar:
    st.header("Configuration")

    if not os.getenv("OPENAI_API_KEY"):
        st.error("Missing OpenAI API Key in .env file")
        st.stop()

    st.success("API Key Detected")

    uploaded_file = st.file_uploader("Upload Data Source", type=("csv"))

    if st.button("Clear Chat History"):
        st.session_state.messages = []

# --- Logic: Handle File Upload ---
if uploaded_file:
    # Save uploaded file to temp path for processing
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    try:
        # Only process if the file has changed to save resources
        if (
            "current_file" not in st.session_state
            or st.session_state.current_file != uploaded_file.name
        ):
            with st.spinner("Vectorizing data and building knowledge base..."):
                # Delegate heavy lifting to the backend
                num_chunks = st.session_state.rag_engine.ingest_file(tmp_file_path)

                st.session_state.current_file = uploaded_file.name
                st.success(f"Knowledge Base Ready! Indexed {num_chunks} chunks.")

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

    # Response placeholder - Retrieval logic goes here in the next step
    response = "Vector Store Active. Ready for retrieval logic."
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
