import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from src.rag_engine import RAGEngine

load_dotenv()

st.set_page_config(page_title="Insight Flow", page_icon="📊", layout="wide")

# --- SIDEBAR CONFIGURATION (Senior Polish) ---
with st.sidebar:
    st.header("⚙️ Configuration")

    # 1. Temperature Slider (Creativity Control)
    temperature = st.slider("Model Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.1, help="0 = Precise, 1 = Creative")

    # 2. Clear Chat Button
    if st.button("Clear Chat History", type="primary"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # File Uploader
    st.subheader("Upload Data Source")
    uploaded_file = st.file_uploader("Upload a CSV", type="csv")

# --- INITIALIZATION ---
if "rag_engine" not in st.session_state:
    # Pass the sidebar temperature to the engine
    st.session_state.rag_engine = RAGEngine(temp=temperature)

# Re-initialize engine if temperature changes (Optional optimization: only re-init LLM)
if st.session_state.rag_engine.llm.temperature != temperature:
     st.session_state.rag_engine = RAGEngine(temp=temperature)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MAIN UI ---
st.title("Insight Flow 📊")
st.caption("One Buffalo Labs | RAG-based Analysis Engine")

# Handle File Upload
if uploaded_file:
    # Save to temp file needed for CSVLoader
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    # Ingest only if not already ingested (simple check)
    if "current_file" not in st.session_state or st.session_state.current_file != uploaded_file.name:
        with st.spinner("Processing data..."):
            st.session_state.rag_engine.ingest_file(tmp_path)
            st.session_state.current_file = uploaded_file.name
        st.toast(f"Ingested {uploaded_file.name} successfully!", icon="✅")

    # Cleanup temp file
    os.unlink(tmp_path)

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # If the message has source docs attached, display them
        if "sources" in message:
            with st.expander("🔍 View Source Data"):
                for i, doc in enumerate(message["sources"]):
                    st.markdown(f"**Source {i+1}:**")
                    st.code(doc.page_content, language="csv")

# Chat Input
if prompt := st.chat_input("Ask a question about your data..."):
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # The query method now returns a Dict
            response_payload = st.session_state.rag_engine.query(prompt)
            answer = response_payload["result"]
            sources = response_payload["source_documents"]

            st.markdown(answer)

            # Display sources immediately for the current response
            if sources:
                with st.expander("🔍 View Source Data"):
                    for i, doc in enumerate(sources):
                        st.markdown(f"**Source {i+1}:**")
                        st.code(doc.page_content, language="csv")

    # Save context and sources to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })