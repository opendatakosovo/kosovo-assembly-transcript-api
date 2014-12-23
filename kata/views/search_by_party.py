from flask.views import View
from flask import Response
from elasticsearch import Elasticsearch
import json


class SearchByParty(View):
    def dispatch_request(self, keyword):

        # Create Elasticsearch instance
        es = Elasticsearch()

        '''
        res1 = es.search(index="transcripta", body={
            "facets": {
                "0": {
                    "date_histogram": {
                        "field": "date",
                        "interval": "5m"
                    },
                    "global": True,
                    "facet_filter": {
                        "fquery": {
                            "query": {
                                "filtered": {
                                    "query": {
                                        "query_string": {
                                            "query": "Kryetar"
                                        }
                                    },
                                    "filter": {
                                        "bool": {
                                            "must": [
                                                {
                                                    "match_all": {}
                                                }
                                            ]
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "size": 0
        }
        )
        '''

        '''

        res2 = es.search(index="transcripta", body={
            "facets": {
                "terms": {
                    "terms_stats": {
                        "value_field": "speech_id",
                        "key_field": "party",
                        "size": 10000,
                        "order": "term"
                    },
                    "facet_filter": {
                        "fquery": {
                            "query": {
                                "filtered": {
                                    "query": {
                                        "bool": {
                                            "should": [
                                                {
                                                    "query_string": {
                                                        "query": keyword
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    "filter": {
                                        "bool": {
                                            "must": [
                                                {
                                                    "match_all": {}
                                                }
                                            ]
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "size": 0
        }
        )
        '''

        # Query Elasticsearch
        res = es.search(index="transcripta",doc_type="speech", search_type="count", body={
            "query": {
                "match": {
                    # Match the documents that has the "keyword"
                    "text": keyword
                }
            },
            "aggs": {
                "parties": {
                    "significant_terms": {
                        "field": "party"
                    }
                }
            }
        }
        )
        '''
        result = []

        # Build the json result

        for doc in res['aggregations']['articles_over_time']['buckets']:
            result.append({"date":doc['key_as_string'],"count":doc['doc_count']})
        '''
        return Response(response=json.dumps(res), mimetype='application/json')
