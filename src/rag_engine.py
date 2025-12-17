import os
from dotenv import load_dotenv
from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()


class RAGEngine:
    def __init__(self, temp=0):
        # 1. Initialize OpenAI with dynamic temperature
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo", temperature=temp, api_key=os.getenv("OPENAI_API_KEY")
        )
        self.vector_store = None
        self.retriever = None
        self.qa_chain = None

    def ingest_file(self, file_path):
        loader = CSVLoader(file_path=file_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()
        self.vector_store = Chroma.from_documents(chunks, embeddings)
        self.retriever = self.vector_store.as_retriever()

        # 2. Define the "Senior" System Prompt
        template = """
        You are a Senior Data Analyst for One Buffalo Labs.
        Your goal is to answer questions based ONLY on the provided context below.
        If the answer cannot be found in the context, strictly state "I don't know" without making up information.

        Context: {context}

        Question: {question}

        Helpful Answer:
        """

        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

        # 3. Create Chain with Source Return enabled
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.retriever,
            return_source_documents=True,  # <--- Crucial for transparency
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
        )

    def query(self, query_text):
        if not self.qa_chain:
            return {"result": "Please upload a document first.", "source_documents": []}

        # The chain now returns a dictionary {result: ..., source_documents: ...}
        return self.qa_chain.invoke({"query": query_text})
