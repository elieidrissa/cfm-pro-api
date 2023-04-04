from .models import *
from .serializers import *
from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
# Pagination types
from rest_framework.pagination import (LimitOffsetPagination, 
                                       PageNumberPagination)
from rest_framework.response import Response
# permissions
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from .permissions import (IsCoordOrReadOnly, UpdateOrDeleteNotAllowed,
                          IsProfileOwner, IsCurrentUser, IsCoordOrDirecteur)
# my toolkit
from .utils import get_lots_stats
# filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import LotFilter


class CustomPagination(PageNumberPagination):
    '''Custom Pagination for 'Lot' results'''
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class AddressChoicesPagination(PageNumberPagination):
    '''Custom Pagination for 'territoire', 'groupement' .
        and 'village' results'''
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserCreateView(generics.GenericAPIView):
    permission_classes = () # no permission required
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
    lookup_field = 'user'

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



class NegociantView(viewsets.ModelViewSet):
    queryset = Negociant.objects.all()
    serializer_class = NegociantSerializer
    permission_classes = (IsCoordOrReadOnly,)


class TransporteurView(viewsets.ModelViewSet):
    queryset = Transporteur.objects.all()
    serializer_class = TransporteurSerializer
    permission_classes = (IsCoordOrReadOnly,)


class MineraiView(viewsets.ModelViewSet):
    queryset = Minerai.objects.all()
    serializer_class = MineraiSerializer
    permission_classes = (IsCoordOrReadOnly,)


class CooperativeView(viewsets.ModelViewSet):
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer
    permission_classes = (IsCoordOrReadOnly,)


class AxeView(viewsets.ModelViewSet):
    queryset = Axe.objects.all()
    serializer_class = AxeSerializer
    permission_classes = (IsCoordOrReadOnly,)


class SiteView(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = (IsCoordOrReadOnly,)


class ChantierView(viewsets.ModelViewSet):
    queryset = Chantier.objects.all()
    serializer_class = ChantierSerializer
    permission_classes = (IsCoordOrReadOnly,)

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

class ChefferieView(viewsets.ModelViewSet):
    queryset = Chefferie.objects.all()
    serializer_class = ChefferieSerializer
    pagination_class = AddressChoicesPagination
    http_method_names = ['get', 'head', 'options']

class GroupementView(viewsets.ModelViewSet):
    queryset = Groupement.objects.all()
    serializer_class = GroupementSerializer
    pagination_class = AddressChoicesPagination
    http_method_names = ['get', 'head', 'options']

class VillageView(viewsets.ModelViewSet):
    queryset = Village.objects.all()
    serializer_class = VillageSerializer
    pagination_class = AddressChoicesPagination
    http_method_names = ['get', 'head', 'options']

# # views
# def api_home(request):
#     return JsonResponse(dict)
# # urls.py
# path('', views.api_home)

@api_view(["GET"])
def get_user_and_profile(request, *args, **kwargs):
    # body = request.body
    user_instance =  User.objects.all().order_by('?').first()
    data = {}
    if user_instance:
        data = UserRetrieveSerializer(user_instance).data
    return Response(data)

@api_view(['GET'])
def current_user_lots(request, *args, **kwargs):
    '''Get the following data:
    - all lots added by the current user
    - total of poids
    - total of colis'''
    user = request.user
    queryset = Lot.objects.filter(user=user)
    # stats
    data = get_lots_stats(queryset)
    # lots data
    serializer = LotDetailSerializer(queryset, many=True)
    serialized_qs = serializer.data
    # response data
    data.update({'lots':serialized_qs})
    return Response(data)



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
