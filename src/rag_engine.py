import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()


class RAGEngine:
    def __init__(self):
        # Ensure API key is available before initializing components
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found. Please check your .env file.")

        self.embeddings = OpenAIEmbeddings()
        self.persist_directory = "./chroma_db"
        self.vector_store = None

    def ingest_file(self, file_path: str) -> int:
        """
        Process the file: Load -> Split -> Embed -> Store.
        Returns the number of chunks created.
        """
        # Clear existing vector store to prevent data pollution between uploads
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)

        # 1. Load Data
        loader = CSVLoader(file_path=file_path)
        raw_documents = loader.load()

        # 2. Split Data
        # Using a 1000/200 split to ensure context is maintained across chunk boundaries
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        chunks = text_splitter.split_documents(raw_documents)

        # 3. Embed & Store
        # Chroma handles the embedding calls implicitly via the passed embedding function
        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
        )

        return len(chunks)
