from elasticsearch import Elasticsearch, helpers


def update_entry(session: Elasticsearch, index, document_id, body):
    """
    Update a document in OpenSearch.
    """

    updated_document = session.update(
        index=index,
        id=document_id,
        body={'doc': body},
        retry_on_conflict=3
    )

    return updated_document


def bulk_update(session, index, body):
    """
    Update multiple documents in OpenSearch.
    """

    bulk_actions = []

    for document in body:
        bulk_actions.append({
            '_op_type': 'update',
            '_index': index,
            '_id': document['id'],
            'doc': document
        })

    updated_documents = helpers.bulk(session, bulk_actions, request_timeout=180)

    return updated_documents


def update_by_query(session, index, query, body_update, params=None):
    """
    Update documents in OpenSearch by query.
    """

    body = {
        'query': query,
        'script': {
            'source': body_update,
        }
    }

    if params:
        body['script']['params'] = params

    updated_documents = session.update_by_query(
        index=index,
        body=body,
        conflicts='proceed'
    )

    return updated_documents