import os
import nltk
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

def chunk_and_index_file(file, indexer, embed_model):
    text = file.read()
    chunks = chunking_text(text)
    embeddings = embed_model.encode(chunks)
    indexer.index_chunks(chunks, embeddings)


def chunk_and_index_rails_docs():
    directory = "/opt/airflow/data/"
    indexer = RailsDocESIndex()
    model = SentenceTransformer('multi-qa-distilbert-cos-v1')

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        print(f"Processing {filepath}")
        if os.path.isfile(filepath):
            with open(filepath, "r") as file:
                chunk_and_index_file(file, indexer, model)
