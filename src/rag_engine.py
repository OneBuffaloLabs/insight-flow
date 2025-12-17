import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# Load env variables immediately
load_dotenv()


class RAGEngine:
    def __init__(self):
        # Validation: Check for API Key
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found. Please check your .env file.")

        # Initialize the LLM
        # We use 'gpt-3.5-turbo' for cost, 'gpt-4o' is the latest/smartest if you have access
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

        # Initialize Embeddings
        self.embeddings = OpenAIEmbeddings()

        self.vector_store = None

    def ingest_file(self, file_path):
        """
        1. Load CSV
        2. Split into chunks
        3. Embed and store in ChromaDB
        """
        # 1. Load
        loader = CSVLoader(file_path=file_path)
        data = loader.load()

        # 2. Split
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100
        )
        chunks = text_splitter.split_documents(data)

        # 3. Vector Store (Chroma)
        # using a local persistence directory so data survives a restart
        self.vector_store = Chroma.from_documents(
            documents=chunks, embedding=self.embeddings, persist_directory="./chroma_db"
        )
        return True
