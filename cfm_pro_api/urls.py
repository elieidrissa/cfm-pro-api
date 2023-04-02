from django.urls import path, include
from rest_framework import routers
from .views import *

router  = routers.DefaultRouter()
router.register('lots', LotView)
router.register('users', UserRetrieveView)
# router.register(r'profile/', UserProfileView)
router.register('negociants', NegociantView)
router.register('transporteurs', TransporteurView)
router.register('minerais', MineraiView)
router.register('coopratives', CooperativeView)
router.register('axes', AxeView)
router.register('sites', SiteView)
router.register('chantiers', ChantierView)
router.register('provinces', ProvinceView)
router.register('territoires', TerritoireView)
router.register('chefferies', ChefferieView)
router.register('groupements', GroupementView)
router.register('villages', VillageView)


urlpatterns = [
    # ALL-user
    path('', include(router.urls)),
    path('auth/', include("rest_framework.urls")), # route /api/auth/login
    path('auth/register', UserCreateView.as_view(), name='sign_up'),
    path('create-lot-list', LotListCreateView.as_view(), name='create_lot_list'),
    path('profile', UserProfileView.as_view({'get': 'list', 'put': 'update'}), name='profile'),
    # path('api/auth/login', UserCreateView.as_view(), name='login'),

    # AT-user
    path('current-user/lots/stats', current_user_lots, name='lots_stats'),
]