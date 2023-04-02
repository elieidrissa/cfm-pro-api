from .models import *
from .serializers import *
from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
# Pagination types
from rest_framework.pagination import (LimitOffsetPagination, 
                                       PageNumberPagination)
from rest_framework.response import Response
# permissions
from .permissions import (IsCoordOrReadOnly, 
                          IsProfileOwner, IsCurrentUser)
from rest_framework.permissions import IsAuthenticated


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

# USER UPDATE
# @login_required
# def profile(request):
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST,
#                                    request.FILES,
#                                    instance=request.user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect('profile')
 
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
 
#     context = {
#         'u_form': u_form,
#         'p_form': p_form
#     }
 
#     return render(request, 'users/profile.html', context)

class UserCreateView(generics.GenericAPIView):
    permission_classes = () # no permission required
    serializer_class = UserCreateSerializer

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
    
    
class UserProfileListView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    pagination_class = CustomPagination
    serializer_class = UserProfileSerializer
    permission_classes = (IsProfileOwner, IsAuthenticated)



class UserRetrieveView(viewsets.ModelViewSet):
    '''Only return the current user's details'''
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = (IsCurrentUser,)

class UserRetrieveListView(viewsets.ModelViewSet):
    '''Gives the list of all users to the 'coord' level users'''
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = (IsCoordOrReadOnly,)


class LotView(viewsets.ModelViewSet):
    '''Retrieve Lots'''
    permission_classes = (IsCoordOrReadOnly,)
    queryset = Lot.objects.all()
    serializer_class = LotSerializer
    pagination_class = CustomPagination


class LotListCreateView(generics.ListCreateAPIView):
    '''This view is used to POST many lots as a list'''
    queryset = Lot.objects.all()
    serializer_class = LotSerializer
    pagination_class = LimitOffsetPagination

    def list(self, request):
        queryset = self.get_queryset()
        serializer = LotSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        data = request.data
        if isinstance(data, list): 
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class NegociantView(viewsets.ModelViewSet):
    queryset = Negociant.objects.all()
    serializer_class = NegociantSerializer


class TransporteurView(viewsets.ModelViewSet):
    queryset = Transporteur.objects.all()
    serializer_class = TransporteurSerializer


class MineraiView(viewsets.ModelViewSet):
    queryset = Minerai.objects.all()
    serializer_class = MineraiSerializer


class CooperativeView(viewsets.ModelViewSet):
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer


class AxeView(viewsets.ModelViewSet):
    queryset = Axe.objects.all()
    serializer_class = AxeSerializer


class SiteView(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class ChantierView(viewsets.ModelViewSet):
    queryset = Chantier.objects.all()
    serializer_class = ChantierSerializer

# -------------------------------------------------------------------------------
# TERRITORIES AND SUB_TERRITORIES
# -------------------------------------------------------------------------------

class ProvinceView(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer


class TerritoireView(viewsets.ModelViewSet):
    queryset = Territoire.objects.all()
    serializer_class = TerritoireSerializer
    pagination_class = AddressChoicesPagination


class ChefferieView(viewsets.ModelViewSet):
    queryset = Chefferie.objects.all()
    serializer_class = ChefferieSerializer
    pagination_class = AddressChoicesPagination


class GroupementView(viewsets.ModelViewSet):
    queryset = Groupement.objects.all()
    serializer_class = GroupementSerializer
    pagination_class = AddressChoicesPagination


class VillageView(viewsets.ModelViewSet):
    queryset = Village.objects.all()
    serializer_class = VillageSerializer
    pagination_class = AddressChoicesPagination

# # views
# def api_home(request):
#     return JsonResponse(dict)
# # urls.py
# path('', views.api_home)

user_data = {
    "nom": "",
    "postnom": "",
    "prenom": "",
    "phone_number": "",
    "password": "",
    "is_AT": "",
    "is_DG": "",
    "is_COORD": "",
    "email": "",
    "sex": "",
    "birth_date": "",
    "birth_place": "",
}


@api_view(["GET"])
def get_user_and_profile(request, *args, **kwargs):
    # body = request.body
    user_instance =  User.objects.all().order_by('?').first()
    data = {}
    if user_instance:
        data = UserRetrieveSerializer(user_instance).data
    return Response(data)

# @api_view(["POST"])
# def create_user_and_profile(request, *args, **kwargs):
#     body = request.data
#     data = {}
#     try:
#         data = json.loads(body)
#     except:
#         pass
#     return Response(data)

def update_user_and_profile(request, *args, **kwargs):

    # body = request.body
    # data = {}
    # try:
    #     data = json.loads(body)
    # except:
    #     pass
    # return JsonResponse(data)
    pass


def get_lots_stats(queryset):
    '''Extract stats from a given lots' 'queryset' '''
    stats ={'sum_poids_Ta':0,
            'sum_poids_Sn':0,
            'sum_poids_W':0,
            'sum_colis_Ta':0,
            'sum_colis_Sn':0,
            'sum_colis_W':0}
    for obj in queryset:
        if obj.minerai.symbol == 'Ta':
            stats['sum_poids_Ta'] += obj.poids
            stats['sum_colis_Ta'] += obj.colis
        elif obj.minerai.symbol == 'Sn':
            stats['sum_poids_Sn'] += obj.poids
            stats['sum_colis_Sn'] += obj.colis
        elif obj.minerai.symbol == 'W':
            stats['sum_poids_W'] += obj.poids
            stats['sum_colis_W'] += obj.colis
    return stats


@api_view(['GET'])
def current_user_lots(request, *args, **kwargs):
    '''Get the following data: 
    - all lots added by the current user
    - sum of poids
    - sum of colis'''
    user = request.user
    queryset = Lot.objects.filter(user=user)
    # stats
    data = get_lots_stats(queryset)
    # lots data
    serializer = LotSerializer(queryset, many=True)
    serialized_qs = serializer.data
    # response data
    data.update({'lots':serialized_qs})
    return Response(data)



