import django_filters
from django_filters.rest_framework import DateFromToRangeFilter
from django_filters import rest_framework as filters
from .models import Negociant, Lot

class NegociantFilter(django_filters.FilterSet):
    class Meta:
        model = Negociant
        fields = ['nom', 'postnom']


class LotFilter(django_filters.FilterSet):

    class Meta:
        model = Lot
        fields = {
            'date' : ('exact', 'lte', 'gte'),
            'user__nom' : ['icontains'], 
            'user__postnom' : ['icontains'],
            'user__prenom' : ['icontains'],
            'negociant__nom' : ['icontains'], 
            'negociant__postnom' : ['icontains'],
            'negociant__prenom' : ['icontains'],
            'minerai__symbol' : ['icontains'],
            'tags' : ['icontains'],
            'atm' : ['icontains'],
            'chantier__name' : ['exact', 'icontains'],
            'chantier__site__name' : ['icontains'],
            'cooperative__short_name' : ['exact', 'icontains'],
            'transporteur__nom' : ['icontains'],
            'transporteur__postnom' : ['icontains'],
            'transporteur__prenom' : ['icontains'],
            'confirmed' : ['exact'],
            'date_submit' : ('exact', 'lte', 'gte'),
            'date_confirm' : ('exact', 'lte', 'gte')
        }

# class LotFilter(django_filters.FilterSet):

#     date = filters.DateFromToRangeFilter(field_name="date", 
#                                          lookup_expr=('exact', 'lte', 'gte'))
#     user = filters.CharFilter(field_name='user__nom', lookup_expr='icontains')
#     # date_submit = filters.DateFromToRangeFilter(field_name="date_submit")

#     class Meta:
#         model = Lot
#         fields = ['user__nom', 'date']
        
        # {
        #     'user__nom' : ['exact', 'icontains'], 
        #     'user__postnom' : ['icontains'],
        #     'user__prenom' : ['icontains'],
        #     'negociant__nom' : ['icontains'], 
        #     'negociant__postnom' : ['icontains'],
        #     'negociant__prenom' : ['icontains'],
        #     'minerai__symbol' : ['icontains'],
        #     'tags' : ['icontains'],
        #     'atm' : ['icontains'],
        #     'chantier__name' : ['icontains'],
        #     'chantier__site__name' : ['icontains'],
        #     'cooperative__short_name' : ['icontains'],
        #     'transporteur__nom' : ['icontains'],
        #     'transporteur__postnom' : ['icontains'],
        #     'transporteur__prenom' : ['icontains'],
        #     'confirmed' : ['icontains'],
        #     'date_submit' : ('exact', 'lte', 'gte'),
        #     'date_confirm' : ('exact', 'lte', 'gte')
        # }
