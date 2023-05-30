import copy

from flask import current_app

from app.utils.opensearch_utils.indices.templates import BASE_TEMPLATE


def create_document_index_template():

    index = copy.deepcopy(BASE_TEMPLATE)

    index['index'] = current_app.config['DOCUMENT_INDEX']

    index['knn'] = False

    similarity = {
        "similarity": {
            "b_05_similarity": {
                "type": "BM25",
                "b": 0.5,
            }
        }
    }

    custom_analyzer = {
        "index": {
            "analysis": {
                "analyzer": {
                    "custom_analyzer": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "english_stop",
                            "english_stemmer",
                            "english_possessive_stemmer"
                        ]
                    }
                },
                "filter": {
                    "english_stop": {
                        "type": "stop",
                        "stopwords": "_english_"
                    },
                    "english_stemmer": {
                        "type": "stemmer",
                        "language": "english"
                    },
                    "english_possessive_stemmer": {
                        "type": "stemmer",
                        "language": "possessive_english"
                    }
                }
            }
        }
    }

    field_mappings = {
        "id": {
            "type": "keyword",
        },
        "content": {
            "type": "text",
            "similarity": "b_05_similarity",
            "fields": {
                "english": {
                    "type": "text",
                    "analyzer": "custom_analyzer",
                },
                "keyword": {
                    "type": "keyword",
                    "ignore_above": 256,
                }
            },
            "term_vector": "yes",
        },
        "vector_embedding": {
            "type": "knn_vector",
            "dimension": current_app.config['KNN_DIMENSIONS'],
        },
        "created_at": {
            "type": "datetime",
            "format": "yyyy-MM-dd HH:mm:ss",
        },
        "updated_at": {
            "type": "datetime",
            "format": "yyyy-MM-dd HH:mm:ss",
        },
    }

    index['body']['mappings']['properties'].update(field_mappings)
    index['body']['settings'].update(custom_analyzer)
    index['body']['settings']['index'].update(similarity)

    return index
