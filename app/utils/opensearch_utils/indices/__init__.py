def create_index(session, template):
    """
    Create an Elasticsearch index.

    :param session: the current elasticsearch session object
    :param template: the template to use for the index
    :return: the response object from elasticsearch
    """

    created = session.indices.create(index=template['index'], body=template['body'])

    return created


def delete_index(session, index):
    """
    Delete an index from Elasticsearch.

    :param session: The Elasticsearch session.
    :param index: The index to delete.
    :return: The response object from elasticsearch.
    """

    deleted_index = session.indices.delete(index=index)

    return deleted_index


def index_exists(session, index):
    """
    Checks if an index exists.
    """

    exists = session.indices.exists(index=index)

    return exists


def reindex(session, source_index, target_index):
    """
    Reindexes an index to a new index.
    """

    reindexed = session.reindex(source_index=source_index, target_index=target_index)

    return reindexed
