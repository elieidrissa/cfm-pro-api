import django_filters
# from django_filters.rest_framework import DateFromToRangeFilter
# from django_filters import rest_framework as filters
from .models import (Negociant, Lot, Transporteur, Minerai, Site, Chantier,
                     Territoire, Chefferie, Groupement, Village)

LOOKUP_EXPR = ['exact', 'icontains']


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


class NegociantFilter(django_filters.FilterSet):
    class Meta:
        model = Negociant
        fields = {
            'nom' : LOOKUP_EXPR, 
            'postnom' : LOOKUP_EXPR,
            'prenom' : LOOKUP_EXPR,
            'phone_number' : LOOKUP_EXPR,
            'birth_date' : ('exact', 'lte', 'gte'),
            'birth_place__name' : LOOKUP_EXPR,
            'sex' : LOOKUP_EXPR,
            'address_info' : LOOKUP_EXPR,
            'address__name' : LOOKUP_EXPR,
            'date_added' : ('exact', 'lte', 'gte'),
            'date_updated' : ('exact', 'lte', 'gte'),
        }


class TransporteurFilter(django_filters.FilterSet):
    class Meta:
        model = Transporteur
        fields = {
            'nom' : LOOKUP_EXPR, 
            'postnom' : LOOKUP_EXPR,
            'prenom' : LOOKUP_EXPR,
            'sex' : LOOKUP_EXPR,
            'negociant__nom' : LOOKUP_EXPR,
            'phone_number' : LOOKUP_EXPR,
            'authorisation' : LOOKUP_EXPR,
            'address__name' : LOOKUP_EXPR,
            'address_info' : LOOKUP_EXPR,
            'plates' : LOOKUP_EXPR,
            'date_added' : ('exact', 'lte', 'gte'),
            'date_updated' : ('exact', 'lte', 'gte'),
        }


class MineraiFilter(django_filters.FilterSet):
    class Meta:
        model = Minerai
        fields = {
            'name' : LOOKUP_EXPR, 
            'symbol' : LOOKUP_EXPR,
            'formule' : LOOKUP_EXPR,
            'date_added' : ('exact', 'lte', 'gte'),
            'date_updated' : ('exact', 'lte', 'gte'),
        }


class SiteFilter(django_filters.FilterSet):
    class Meta:
        model = Site
        fields = {
            'name' : LOOKUP_EXPR, 
            'axe__name' : LOOKUP_EXPR,
            'village__name' : LOOKUP_EXPR,
            'date_added' : ('exact', 'lte', 'gte'),
            'date_updated' : ('exact', 'lte', 'gte'),
        }


class ChantierFilter(django_filters.FilterSet):
    class Meta:
        model = Chantier
        fields = {
            'name' : LOOKUP_EXPR, 
            'longitude' : LOOKUP_EXPR,
            'latitude' : LOOKUP_EXPR,
            'site__name' : LOOKUP_EXPR,
            'date_added' : ('exact', 'lte', 'gte'),
            'date_updated' : ('exact', 'lte', 'gte'),
        }


# ADDRESS
class TerritoireFilter(django_filters.FilterSet):
    class Meta:
        model = Territoire
        fields = {
            'name' : LOOKUP_EXPR, 
            'province__name' : LOOKUP_EXPR,
            'date_added' : ('exact', 'lte', 'gte'),
            'date_updated' : ('exact', 'lte', 'gte'),
        }


class ChefferieFilter(django_filters.FilterSet):
    class Meta:
        model = Chefferie
        fields = {
            'name' : LOOKUP_EXPR, 
            'territoire__name' : LOOKUP_EXPR,
            'date_added' : ('exact', 'lte', 'gte'),
            'date_updated' : ('exact', 'lte', 'gte'),
        }


class GroupementFilter(django_filters.FilterSet):
    class Meta:
        model = Groupement
        fields = {
            'name' : LOOKUP_EXPR, 
            'chefferie__name' : LOOKUP_EXPR,
            'date_added' : ('exact', 'lte', 'gte'),
            'date_updated' : ('exact', 'lte', 'gte'),
        }


class VillageFilter(django_filters.FilterSet):
    class Meta:
        model = Village
        fields = {
            'name' : LOOKUP_EXPR, 
            'groupement__name' : LOOKUP_EXPR,
            'date_added' : ('exact', 'lte', 'gte'),
            'date_updated' : ('exact', 'lte', 'gte'),
        }
