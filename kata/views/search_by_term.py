from flask.views import View
from flask import Response
from elasticsearch import Elasticsearch
import json
from datetime import datetime


class SearchByTerm(View):
    def dispatch_request(self, keyword):

        # Create Elasticsearch instance
        es = Elasticsearch()

        # Query Elasticsearch
        res = es.search(index="transcripta",search_type="count", body={
            "query": {
                "match": {
                    # Match the documents that has the "keyword"
                    "text": keyword
                }
            },
            "aggs": {
                "articles_over_time": {
                    "date_histogram": {
                        "field": "date",
                        "interval": "1M",
                        "format": "yyyy-MM-dd"
                    }
                }
            }
        }
        )

        result = []

        # Build the json result
        for doc in res['aggregations']['articles_over_time']['buckets']:
            result.append({"date":doc['key_as_string'],"count":doc['doc_count']})

        return Response(response=json.dumps(result), mimetype='application/json')
