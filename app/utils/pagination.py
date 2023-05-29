from flask_sqlalchemy import BaseQuery, Pagination


def paginate(query: BaseQuery, page: int, per_page: int, starting_id: int = None, shallow: bool = True):
    """
    Paginate a query

    :param query: SQLAlchemy Query Object to paginate.
    :param page: Page number.
    :param per_page: Items per page.
    :param starting_id: Starting ID value to filter by to improve performance.
    :param shallow: Convert items to dictionary to avoid lazy loading during deserialization.
    :return: Pagination object.
    """

    offset = (page - 1) * per_page
    query = query.limit(per_page + 1).offset(starting_id or offset)

    count = query.count() + offset
    items = query.all()

    if shallow:
        items = [{k: v for k, v in vars(entry).items() if k != '_sa_instance_state'} for entry in items]

    return Pagination(
        query=query,
        page=page,
        per_page=per_page,
        total=count,
        items=items
    )


def get_pagination_info(page, per_page, total):
    max_pages = min(total // per_page + 1, 1000)
    pages = str(min(total // per_page + 1, 10000 // per_page))

    return {
        'has_next': page < max_pages,
        'has_prev': page > 1,
        'next_num': str(min(page + 1, max_pages)) if page < max_pages else None,
        'prev_num': str(page - 1) if page > 1 else None,
        'pages': pages,
        'total': str(min(total, 10000)),
    }