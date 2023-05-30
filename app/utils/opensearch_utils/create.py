from elasticsearch import helpers


def create_entry(session, index, body, document_id=None):
    """
    Create a document in OpenSearch.

    :param session: The OpenSearch session.
    :param document_id: The document id.
    :param body: The document body.
    :param index: The index to create the document in.
    :return: The created document.
    """

    if document_id:
        created = session.index(
            index=index,
            id=document_id,
            body=body
        )
    else:
        created = session.index(
            index=index,
            body=body
        )

    return created


def bulk_create_entries(session, documents, index):
    """
    Create multiple documents in OpenSearch.

    :param session: The OpenSearch session.
    :param documents: The documents to create.
    :param index: The index to create the documents in.
    :return: The created documents.
    """

    bulk_actions = []

    for document in documents:
        if document.get('id'):
            bulk_actions.append({
                '_index': index,
                '_id': document['id'],
                '_source': document
            })
        else:
            bulk_actions.append({
                '_index': index,
                '_source': document
            })

    created = helpers.bulk(session, bulk_actions, request_timeout=180)

    return created