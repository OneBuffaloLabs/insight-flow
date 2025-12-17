from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def ingest_file(file_path):
    # Load the data
    loader = CSVLoader(file_path=file_path)
    raw_documents = loader.load()

    # Split the text
    # We split into chunks of 1000 characters with 200 overlap to maintain context
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    documents = text_splitter.split_documents(raw_documents)

    return documents
