from elasticsearch import Elasticsearch, ElasticsearchException
from flask import current_app


def opensearch_session():
    """
    Returns an OpenSearch session.
    """

    # Check if the required config variables are set
    try:
        opensearch_url = current_app.config.get('OPENSEARCH_URL')
        opensearch_user = current_app.config.get('OPENSEARCH_USER')
        opensearch_password = current_app.config.get('OPENSEARCH_PASSWORD')

        if not all([opensearch_url, opensearch_user, opensearch_password]):
            raise ValueError("One or more config variables are not set.")
    except KeyError as e:
        raise ValueError(f"Config variable {e.args[0]} is not set.")

    # Create the session
    try:
        session = Elasticsearch([opensearch_url],
                                http_auth=(opensearch_user,
                                           opensearch_password))
    except ElasticsearchException as e:
        raise ConnectionError("Could not connect to OpenSearch: " + str(e))

    if session is None:
        raise ValueError("Elasticsearch session is None.")

    return session
