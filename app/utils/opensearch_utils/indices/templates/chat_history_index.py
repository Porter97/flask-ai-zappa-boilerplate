import copy

from flask import current_app

from app.utils.opensearch_utils.indices.templates import BASE_TEMPLATE


def create_chat_history_index_template():

    index = copy.deepcopy(BASE_TEMPLATE)

    index['index'] = current_app.config['CHAT_HISTORY_INDEX']

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
        'id': {
            'type': 'keyword',
        },
        'user_id': {
            'type': 'keyword',
        },
        'document_id': {
            'type': 'keyword',
        },
        'timestamp': {
            'type': 'date',
            'format': 'yyyy-MM-dd HH:mm:ss',
        },
        'role': {
            'type': 'keyword',
        },
        'content': {
            'type': 'text',
            'similarity': 'b_05_similarity',
            'fields': {
                "english": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
                },
                "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                }
            },
            "term_vector": "yes"
        },
        "vector_embedding": {
            "type": "knn_vector",
            "dimension": current_app.config['KNN_DIMENSIONS'],
        },
    }

    index['body']['mappings']['properties'].update(field_mappings)
    index['body']['settings'].update(custom_analyzer)
    index['body']['settings']['index'].update(similarity)

    return index