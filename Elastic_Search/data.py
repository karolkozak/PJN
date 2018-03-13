YEAR = "2013"
BASE_URL = "http://localhost:9200"
ALL_JUDGMENTS = list()
JUDGMENTS = list()

INDEX_BODY = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
        "analysis": {
            "analyzer": {
                "my_custom_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "morfologik_stem",
                    ]
                }
            }
        },
    },
    "mappings": {
        "doc": {
            "properties": {
                "textContent": {"type": "text", "analyzer": "my_custom_analyzer"},
                "judgmentDate": {"type": "date"},
                "caseNumber": {"type": "keyword"},
                "judges.name": {"type": "keyword"},
            }
        }
    }
}

INJURY = {
    "query": {
        "match": {
            "textContent": "szkoda"
        }
    }
}

SENTENCE = {
    "query": {
        "match_phrase": {
            "textContent": "trwały uszczerbek na zdrowiu"
        }
    }
}

SENTENCE_SLOP_2 = {
    "query": {
        "span_near": {
            "clauses": [
                {"span_term": {"textContent": "trwały"}},
                {"span_term": {"textContent": "uszczerbek"}},
                {"span_term": {"textContent": "na"}},
                {"span_term": {"textContent": "zdrowie"}}
            ],
            "slop": 2,
            "in_order": True
        }
    }
}


JUDGES_AGGS = {
    "size": 0,
    "aggs": {
        "group_by_judge": {
            "terms": {
                "field": "judges.name"
            }
        }
    }
}

MONTH_AGGS = {
    "aggs": {
        "judgments_per_month": {
            "date_histogram": {
                "field": "judgmentDate",
                "interval": "month"
            }
        }
    }
}


def clear_all_judgments():
    global ALL_JUDGMENTS
    ALL_JUDGMENTS = list()
