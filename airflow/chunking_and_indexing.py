import os
import nltk
import uuid
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from rails_doc_es_index import RailsDocESIndex

def chunking_text(text, max_chunk_size=1000, overlap=100):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_size = 0

    for sentence in sentences:
        sentence_size = len(sentence)
        if current_size + sentence_size > max_chunk_size:
            chunk_text = " ".join(current_chunk)
            chunks.append(chunk_text)

            # Calculate overlap
            overlap_size = 0
            while overlap_size < overlap and current_chunk:
                overlap_size += len(current_chunk[-1])
                current_chunk = current_chunk[-1:]

            current_size = overlap_size

        current_chunk.append(sentence)
        current_size += sentence_size

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def create_index(chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    # Add vectors to the index
    index.add(embeddings)

    return index

def chunk_and_index_file(file, indexer, embed_model):
    text = file.read()
    chunks = chunking_text(text)
    embeddings = model.encode(chunks)
    indexer.index_chunks(chunks, embeddings)

# Usage example
with open("data/bs4/index.txt", "r") as file:
    text = file.read()
    chunks = chunking_text(text)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}: {chunk[:50]}...")  # Print first 50 characters of each chunk


def run():
    indexer = RailsDocESIndex()
    model = SentenceTransformer('all-MiniLM-L6-v2')

    directory = "data/bs4/"
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        print(f"Processing {filepath}")
        if os.path.isfile(filepath):
            with open(filepath, "r") as file:
                chunk_and_index_file(file, indexer, model)

# Search example
    query = "How to use ActiveRecord?"
    query_embedding = model.encode([query])[0]
    results = indexer.search(query, query_embedding)

    print(results)
