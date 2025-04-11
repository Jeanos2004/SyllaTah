from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class CustomPagination(PageNumberPagination):
    """
    Pagination personnalisée avec des métadonnées supplémentaires
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('total_pages', self.page.paginator.num_pages),
            ('current_page', self.page.number),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('page_size', self.get_page_size(self.request)),
            ('has_next', self.page.has_next()),
            ('has_previous', self.page.has_previous())
        ]))

    def get_page_size(self, request):
        if request.user.is_authenticated and request.user.is_lodge_admin:
            return min(int(request.query_params.get(self.page_size_query_param, 20)), self.max_page_size)
        return super().get_page_size(request)

class LargeResultSetPagination(CustomPagination):
    """
    Pagination pour les grands ensembles de données
    """
    page_size = 50
    max_page_size = 200
