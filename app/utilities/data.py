from .logger import logger


def m_dumps(cls, data: object):
    return data.model_dump()


def m_dumps_unset(cls, data: object):
    return data.model_dump(exclude_unset=True)


def set_empty_strs_null(cls, values: object):
    """
    Ignore optional fields == None
    Set field signaled to be reset to None with ""
    """
    items = values.model_dump(exclude_none=True)
    for key in items:
        if items[key] == "":
            items[key] = None
    return items


def record_exists(cls, instance: object, exception: Exception) -> bool:
    if instance:
        class_name = exception.__name__
        logger.warning(
            f"Warning: record already exists, a duplicate entry is not allowed for {class_name}"
        )
        raise exception()
    return instance


def record_not_exist(cls, instance: object, exception: Exception) -> bool:
    if not instance:
        class_name = exception.__name__
        logger.warning(f"Warning: record not found for {class_name}")
        raise exception()
    return instance
