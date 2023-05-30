from flask import current_app

BASE_TEMPLATE = {
    'index': '',
    'body': {
        'settings': {
            'number_of_shards': current_app.config.get('OPENSEARCH_SHARDS', 1),
            'number_of_replicas': current_app.config.get('OPENSEARCH_REPLICAS', 0),
        },
        'mappings': {
            'properties': {}
        }
    }
}