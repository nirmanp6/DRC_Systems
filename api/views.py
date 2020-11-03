from rest_framework import viewsets, filters

from .serializers import ProductSerializer
from products.models import product


class ProductViewSet(viewsets.ModelViewSet):
    '''Viewset to display product data
    extracted in json format via api'''
    # define column to search on
    search_fields = ['name']
    # set filterbackend
    filter_backends = (filters.SearchFilter,)
    queryset = product.objects.all().order_by('id')
    # import serializer to convert model to json
    serializer_class = ProductSerializer
