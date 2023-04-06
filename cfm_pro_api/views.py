from .models import *
from .serializers import *
# from django.shortcuts import render
# from rest_framework.decorators import action, api_view
from rest_framework import generics, status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
# pagination types
from rest_framework.response import Response
from rest_framework.pagination import (LimitOffsetPagination, 
                                       PageNumberPagination)
# permissions
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from .permissions import (IsCoordOrReadOnly, UpdateOrDeleteNotAllowed,
                          IsProfileOwner, IsCurrentUser, IsCoordOrDirecteur)
# filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import (LotFilter, NegociantFilter, TransporteurFilter, 
                      MineraiFilter, SiteFilter, ChantierFilter,
                      TerritoireFilter, ChefferieFilter, GroupementFilter,
                      VillageFilter)
# my toolkit
# from .utils import get_lots_stats


class CustomPagination(PageNumberPagination):
    '''Custom Pagination for 'Lot' results'''
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class AddressChoicesPagination(PageNumberPagination):
    '''Custom Pagination for 'territoire', 'groupement' .
        and 'village' results'''
    page_size = 300
    page_size_query_param = 'page_size'
    max_page_size = 100

# -------------------------------------------------------------------------------
# USER-VIEWS
# -------------------------------------------------------------------------------
# !!!!!!!!!!!!!!!CHANGE ALLOWED METHODS
class UserZoneListView(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = UserZoneSerializer
    permission_classes = () # no permission/read_only
    http_method_names = ['get', 'head', 'options']


class UserCreateView(generics.GenericAPIView):
    permission_classes = () # no permission/post_only
    serializer_class = UserCreateSerializer
    http_method_names = ['post']

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileView(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = (IsProfileOwner, IsAuthenticated)

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    
    # override this method since there's no <pk> in the profile table
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's belows
        obj = queryset.get(user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        data = request.data
        serializer = self.serializer_class(instance=instance,
                                            data=data,
                                            # context={'author': user},
                                            partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserProfileListView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    pagination_class = CustomPagination
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'head', 'options']


class UserRetrieveView(viewsets.ModelViewSet):
    '''Only return the current user's details'''
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = (IsCurrentUser,)

class UserRetrieveListView(viewsets.ModelViewSet):
    '''Gives the list of all users to the 'coord' level users'''
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    http_method_names = ['get', 'head', 'options']

# -------------------------------------------------------------------------------
# LOTS-VIEWS
# -------------------------------------------------------------------------------
class LotHyperlinkedView(viewsets.ModelViewSet):
    '''Retrieve Lots'''
    permission_classes = (IsCoordOrReadOnly, )
    queryset = Lot.objects.all()
    serializer_class = LotHyperlinkedSerializer
    pagination_class = CustomPagination
    # pagination_class = LimitOffsetPagination


class LotModelView(viewsets.ModelViewSet):
    '''Retrieve Lots with details'''
    permission_classes = (IsCoordOrReadOnly,)
    queryset = Lot.objects.all()
    serializer_class = LotModelSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)


class LotCustomView(viewsets.ModelViewSet):
    '''Retrieve Lots with details'''
    permission_classes = (IsCoordOrReadOnly,)
    queryset = Lot.objects.all()
    serializer_class = LotDetailSerializer
    pagination_class = CustomPagination


class LotListCreateView(generics.ListCreateAPIView):
    '''This view is used to POST as list of lots'''
    queryset = Lot.objects.all()
    serializer_class = LotModelSerializer
    pagination_class = CustomPagination
    # pagination_class = LimitOffsetPagination
    http_method_names = ['post']


class LotCustomView(viewsets.ModelViewSet):
    '''filter lots by URL params'''
    permission_classes = (IsCoordOrDirecteur,)
    queryset = Lot.objects.all()
    serializer_class = LotDetailSerializer
    pagination_class = CustomPagination


class LotFilterListView(ListAPIView):
    '''This view is used to SEARCH through list of lots'''
    serializer_class = LotDetailSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LotFilter

    def get_queryset(self):
        request = self.request
        user = request.user

        # only show 'all lots' to COORD or higher users
        if user.is_COORD or user.is_superuser or user.is_DG:
            qs = Lot.objects.all()
        else:
            qs = Lot.objects.filter(user=user)

        self.filterset = LotFilter(request.GET, queryset=qs)
        return self.filterset.qs

# -------------------------------------------------------------------------------
# NEGOCIANTS
# -------------------------------------------------------------------------------
class NegociantView(viewsets.ModelViewSet):
    queryset = Negociant.objects.all()
    serializer_class = NegociantSerializer
    permission_classes = (IsCoordOrReadOnly,)


class NegociantFilterListView(ListAPIView):
    '''This view is used to SEARCH through negociants'''
    queryset = Negociant.objects.all()
    serializer_class = NegociantDetailSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NegociantFilter

    def get_queryset(self):
        req = self.request
        qs = self.queryset
        self.filterset = NegociantFilter(req.GET, queryset=qs)
        return self.filterset.qs

# -------------------------------------------------------------------------------
# TRANSPORTEURS
# -------------------------------------------------------------------------------
class TransporteurView(viewsets.ModelViewSet):
    queryset = Transporteur.objects.all()
    serializer_class = TransporteurSerializer
    permission_classes = (IsCoordOrReadOnly,)


class TransporteurFilterListView(ListAPIView):
    '''This view is used to SEARCH through negociants'''
    queryset = Transporteur.objects.all()
    serializer_class = TransporteurDetailSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TransporteurFilter

    def get_queryset(self):
        req = self.request
        qs = self.queryset
        self.filterset = TransporteurFilter(req.GET, queryset=qs)
        return self.filterset.qs

# -------------------------------------------------------------------------------
# MINERAIS
# -------------------------------------------------------------------------------
class MineraiView(viewsets.ModelViewSet):
    queryset = Minerai.objects.all()
    serializer_class = MineraiSerializer
    permission_classes = (IsCoordOrReadOnly,)


class MineraiFilterListView(ListAPIView):
    '''This view is used to SEARCH through negociants'''
    queryset = Minerai.objects.all()
    serializer_class = MineraiDetailSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MineraiFilter

    def get_queryset(self):
        req = self.request
        qs = self.queryset
        self.filterset = MineraiFilter(req.GET, queryset=qs)
        return self.filterset.qs

# -------------------------------------------------------------------------------
# COOPERATIVES
# -------------------------------------------------------------------------------
# COOPS
class CooperativeView(viewsets.ModelViewSet):
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer
    permission_classes = (IsCoordOrReadOnly,)

# AXES
class AxeView(viewsets.ModelViewSet):
    queryset = Axe.objects.all()
    serializer_class = AxeSerializer
    permission_classes = (IsCoordOrReadOnly,)

# SITES
class SiteView(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = (IsCoordOrReadOnly,)

class SiteFilterListView(ListAPIView):
    '''This view is used to SEARCH through negociants'''
    queryset = Site.objects.all()
    serializer_class = SiteDetailSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SiteFilter

    def get_queryset(self):
        req = self.request
        qs = self.queryset
        self.filterset = SiteFilter(req.GET, queryset=qs)
        return self.filterset.qs

# CHANTIER
class ChantierView(viewsets.ModelViewSet):
    queryset = Chantier.objects.all()
    serializer_class = ChantierSerializer
    permission_classes = (IsCoordOrReadOnly,)

class ChantierFilterListView(ListAPIView):
    '''This view is used to SEARCH through negociants'''
    queryset = Chantier.objects.all()
    serializer_class = ChantierDetailSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ChantierFilter

    def get_queryset(self):
        req = self.request
        qs = self.queryset
        self.filterset = ChantierFilter(req.GET, queryset=qs)
        return self.filterset.qs

# -------------------------------------------------------------------------------
# TERRITORIES AND SUB_TERRITORIES
# -------------------------------------------------------------------------------
class ProvinceView(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    http_method_names = ['get', 'head', 'options']


class TerritoireView(viewsets.ModelViewSet):
    queryset = Territoire.objects.all()
    serializer_class = TerritoireSerializer
    pagination_class = AddressChoicesPagination
    http_method_names = ['get', 'head', 'options']

class TerritoireFilterListView(ListAPIView):
    '''This view is used to SEARCH through negociants'''
    queryset = Territoire.objects.all()
    serializer_class = TerritoireDetailSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TerritoireFilter

    def get_queryset(self):
        req = self.request
        qs = self.queryset
        self.filterset = TerritoireFilter(req.GET, queryset=qs)
        return self.filterset.qs
    
# CHEFFERIE
class ChefferieView(viewsets.ModelViewSet):
    queryset = Chefferie.objects.all()
    serializer_class = ChefferieSerializer
    pagination_class = AddressChoicesPagination
    http_method_names = ['get', 'head', 'options']

class ChefferieFilterListView(ListAPIView):
    '''This view is used to SEARCH through negociants'''
    queryset = Chefferie.objects.all()
    serializer_class = ChefferieDetailSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ChefferieFilter

    def get_queryset(self):
        req = self.request
        qs = self.queryset
        self.filterset = ChefferieFilter(req.GET, queryset=qs)
        return self.filterset.qs

# GROUPEMENT
class GroupementView(viewsets.ModelViewSet):
    queryset = Groupement.objects.all()
    serializer_class = GroupementSerializer
    pagination_class = AddressChoicesPagination
    http_method_names = ['get', 'head', 'options']

class GroupementFilterListView(ListAPIView):
    '''This view is used to SEARCH through negociants'''
    queryset = Groupement.objects.all()
    serializer_class = GroupementDetailSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GroupementFilter

    def get_queryset(self):
        req = self.request
        qs = self.queryset
        self.filterset = GroupementFilter(req.GET, queryset=qs)
        return self.filterset.qs

# VILLAGE
class VillageView(viewsets.ModelViewSet):
    queryset = Village.objects.all()
    serializer_class = VillageSerializer
    pagination_class = AddressChoicesPagination
    http_method_names = ['get', 'head', 'options']

class VillageFilterListView(ListAPIView):
    '''This view is used to SEARCH through negociants'''
    queryset = Village.objects.all()
    serializer_class = VillageDetailSerializer
    pagination_class = AddressChoicesPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = VillageFilter

    def get_queryset(self):
        req = self.request
        qs = self.queryset
        self.filterset = VillageFilter(req.GET, queryset=qs)
        return self.filterset.qs

