from functools import reduce

from django.db.models import Q


def search_model_fulltext(model, fields: list, values: list):
    """
    Perform full-text search on a Django model.
    :param model: The Django model to search.
    :param fields: List of field names to search.
    :param values: List of search query values.
    :return: QuerySet of objects matching the search query.
    """
    search_queries = [
        Q(**{f'{field}__icontains': value}) for value in values
        for field in fields
    ]
    results = model.objects.filter(reduce(lambda a, b: a | b, search_queries))
    return results
