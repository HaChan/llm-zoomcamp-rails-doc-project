import os
import re
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure you have set OPENAI_API_KEY in your environment variables
if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

def extract_text_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        # Remove extra whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def process_files(directory):
    documents = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory)
                text = extract_text_from_html(file_path)
                documents.append({"content": text, "source": relative_path})
    return documents

def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunked_documents = []
    for doc in documents:
        chunks = text_splitter.create_documents([doc["content"]], [doc["source"]])
        chunked_documents.extend(chunks)
    return chunked_documents

def create_vector_store(documents):
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db")
    return vector_store

def main():
    input_directory = "./rails_api_docs"
    documents = process_files(input_directory)
    print(f"Processed {len(documents)} documents")

    chunked_documents = chunk_documents(documents)
    print(f"Created {len(chunked_documents)} chunks")

    vector_store = create_vector_store(chunked_documents)
    print("Vector store created and persisted")

if __name__ == "__main__":
    main()
