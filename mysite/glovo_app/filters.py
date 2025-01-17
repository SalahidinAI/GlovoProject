from django_filters import FilterSet
from .models import *

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'price': ['gt', 'lt']
        }