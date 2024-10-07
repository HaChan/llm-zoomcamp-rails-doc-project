from elasticsearch import Elasticsearch

class RailsDocESIndex:
    def __init__(self, index_name="rails_api_docs"):
        self.es = Elasticsearch("http://elasticsearch:9200")
        self.index_name = index_name

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
