from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class RailsDocESIndex:
    def __init__(self, index_name="rails_api_docs"):
        self.es = Elasticsearch("http://localhost:9200")
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
                        "dims": dims
                        "index": True,
                        "similarity": "cosine"
                    }
                }
            }
        }
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name, body=index_settings)

    def index_chunks(self, chunks, embeddings):
        actions = [
            {
                "_index": self.index_name,
                "_id": str(uuid.uuid4()),
                "_source": {
                    "content": chunk,
                    "embedding": embedding.tolist()
                }
            }
            for chunk, embedding in zip(chunks, embeddings)
        ]
        bulk(self.es, actions)

    def search(self, embedding, top_k=10):
        knn = {
            "field": 'embedding',
            "query_vector": embedding,
            "k": top_k,
            "num_candidates": 10000,
        }
        response = self.es.search(
            index=self.index_name,
            body= {
                'knn': knn,
                "_source": {"includes": ["content"]}
            }
        )

        return [hit["_source"]["content"] for hit in response["hits"]["hits"]]
