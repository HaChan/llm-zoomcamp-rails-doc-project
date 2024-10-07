import uuid
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class RailsDocESIndex:
    def __init__(self, index_name="rails_api_docs"):
        self.es = Elasticsearch("http://elasticsearch:9200")
        self.index_name = index_name
        self.create_index()

    def create_index(self, dims=768):
        index_settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "content": {"type": "text"},
                    "embedding": {
                        "type": "dense_vector",
                        "dims": dims,
                        "index": True,
                        "similarity": "cosine"
                    }
                }
            }
        }
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name, body=index_settings)

    def index_chunks_1(self, chunks, embeddings):
        for chunk, embedding in zip(chunks, embeddings):
            doc = {
                "content": chunk,
                "embedding": embedding
            }
            self.es.index(index=self.index_name, document=doc)

    def index_chunks(self, chunks, embeddings):
        actions = [
            {
                "_index": self.index_name,
                "_id": str(uuid.uuid4()),
                "_source": {
                    "content": chunk,
                    "embedding": embedding
                }
            }
            for chunk, embedding in zip(chunks, embeddings)
        ]
        bulk(self.es, actions)
