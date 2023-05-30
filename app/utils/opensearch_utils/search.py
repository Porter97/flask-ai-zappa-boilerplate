
def entry_exists(session, document_id, index):
    """
    Check if an entry exists in Elasticsearch.

    :param session: The OpenSearch session.
    :param document_id: The document id.
    :return: True if the document exists, False otherwise.
    """

    document_exists = session.exists(
        index=index,
        id=document_id
    )

    return document_exists


def get_entry_by_id(session, document_id, index):
    """
    Get an entry by id from OpenSearch.

    :param session: The OpenSearch session.
    :param document_id: The document id.
    :return: The document.
    """

    document = session.get(
        index=index,
        id=document_id
    )

    return document


def term_vector(session, document_id, index, fields):
    """
    Get the term vector for a document.

    :param session: The OpenSearch session.
    :param document_id: The document id.
    :return: The term vector.
    """

    term_vector = session.termvectors(
        index=index,
        doc_type='_doc',
        fields=fields,
        id=document_id,
        term_statistics=True,
    )

    return term_vector


def multi_get_term_vectors(session, query):
    """
    Get the term vectors for multiple documents.

    :param session: The OpenSearch session.
    :param document_ids: The document ids.
    :return: The term vectors.
    """

    term_vectors = session.mtermvectors(
        body=query
    )

    return term_vectors