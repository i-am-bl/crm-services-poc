def page_offset(page: int, limit: int) -> int:
    """
    Utility function to calculate the offset for pagination.

    :param page: int: page number
    :param limit: int: number of items per page
    :return: int: offset
    """
    return (page - 1) * limit


def has_more_items(total_count: int, page: int, limit: int) -> bool:
    """
    Utility function to determine if there are more items to be displayed.

    :param total_count: int: total number of items
    :param page: int: page number
    :param limit: int: number of items per page
    :return: bool: True if there are more items to be displayed
    """
    return total_count > (page * limit)
