import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

load_dotenv()


class RAGEngine:
    def __init__(self):
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found. Please check your .env file.")

        # Initialize core components
        self.embeddings = OpenAIEmbeddings()
        # Temperature 0 ensures factual consistency for data analysis
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        self.persist_directory = "./chroma_db"
        self.vector_store = None
        self.qa_chain = None

    def ingest_file(self, file_path: str) -> int:
        """
        Full ingestion pipeline: Load CSV -> Split -> Embed -> Store -> Init Chain
        """
        # Clear previous database to ensure clean query context
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)

        loader = CSVLoader(file_path=file_path)
        raw_documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        chunks = text_splitter.split_documents(raw_documents)

        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
        )

        # Re-initialize the retrieval chain with the new data
        self._initialize_chain()

        return len(chunks)

    def _initialize_chain(self):
        """Builds the RetrievalQA chain using the current vector store."""
        if not self.vector_store:
            return

        # Configure retriever to fetch the top 3 most relevant chunks
        retriever = self.vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": 3}
        )

        # "Stuff" chain combines the retrieved chunks into the prompt context
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm, chain_type="stuff", retriever=retriever
        )

    def query(self, question: str) -> str:
        """
        Executes the RAG pipeline:
        Question -> Vector Search -> Context + Question -> LLM -> Answer
        """
        if not self.qa_chain:
            # Handle restart scenarios where DB exists but object is new
            if os.path.exists(self.persist_directory):
                self.vector_store = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings,
                )
                self._initialize_chain()
            else:
                return "Please upload a data file first."

        response = self.qa_chain.invoke({"query": question})
        return response["result"]
