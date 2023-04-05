import django_filters
from django_filters.rest_framework import DateFromToRangeFilter
from django_filters import rest_framework as filters
from .models import Negociant, Lot

LOOKUP_EXPR = ['exact', 'icontains']

class NegociantFilter(django_filters.FilterSet):
    class Meta:
        model = Negociant
        fields = {
            'date' : ('exact', 'lte', 'gte'),
            'nom' : LOOKUP_EXPR, 
            'postnom' : LOOKUP_EXPR,
            'prenom' : LOOKUP_EXPR,
            'phone_number' : LOOKUP_EXPR,
            'birth_date' : ('exact', 'lte', 'gte'),
            'sex' : LOOKUP_EXPR,
            'address__name' : LOOKUP_EXPR,
        }


class LotFilter(django_filters.FilterSet):

    class Meta:
        model = Lot
        fields = {
            'date' : ('exact', 'lte', 'gte'),
            'user__nom' : LOOKUP_EXPR, 
            'user__postnom' : LOOKUP_EXPR,
            'user__prenom' : LOOKUP_EXPR,
            'negociant__nom' : LOOKUP_EXPR, 
            'negociant__postnom' : LOOKUP_EXPR,
            'negociant__prenom' : LOOKUP_EXPR,
            'minerai__symbol' : LOOKUP_EXPR,
            'tags' : LOOKUP_EXPR,
            'atm' : LOOKUP_EXPR,
            'chantier__name' : LOOKUP_EXPR,
            'chantier__site__name' : LOOKUP_EXPR,
            'cooperative__short_name' : LOOKUP_EXPR,
            'transporteur__nom' : LOOKUP_EXPR,
            'transporteur__postnom' : LOOKUP_EXPR,
            'transporteur__prenom' : LOOKUP_EXPR,
            'confirmed' : ['exact'],
            'date_submit' : ('exact', 'lte', 'gte'),
            'date_confirm' : ('exact', 'lte', 'gte')
        }
