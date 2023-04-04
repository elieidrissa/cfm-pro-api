import django_filters
from .models import Negociant, Lot

class NegociantFilter(django_filters.FilterSet):
    nom = django_filters.CharFilter(lookup_expr='icontains')
    postnom = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Negociant
        fields = ['nom', 'postnom']


class LotFilter(django_filters.FilterSet):
    class Meta:
        model = Lot
        fields = {
            'user__nom':['icontains'], 
            'user__postnom':['icontains'],
            'user__prenom':['icontains'],
            'chantier__name':['exact'],
            # 'date_submitted':['icontains'],
        }

# 'chantier__name':['exact']