def delete_entry(session, document_id, index):
    """
    Delete a document from OpenSearch.
    """

    deleted_document = session.delete(
        index=index,
        id=document_id
    )

    return deleted_document


def delete_by_query(session, index, query):
    """
    Delete documents from OpenSearch by query.
    """

    deleted_documents = session.delete_by_query(
        index=index,
        body=query
    )

    return deleted_documents
