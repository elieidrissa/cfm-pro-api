from django.urls import path, include
from rest_framework import routers
from .views import *

router  = routers.DefaultRouter()
# lots
router.register('lots', LotCustomView)
router.register('lots/hyperlinks', LotHyperlinkedView)
router.register('lots/keys', LotModelView)
# router.register()
# users
router.register('users', UserRetrieveListView)
router.register('profiles', UserProfileListView)
# additional data
router.register('negociants', NegociantView)
router.register('transporteurs', TransporteurView)
router.register('minerais', MineraiView)
router.register('coopratives', CooperativeView)
router.register('axes', AxeView)
router.register('sites', SiteView)
router.register('chantiers', ChantierView)
# province, territoires - data
router.register('provinces', ProvinceView)
router.register('territoires', TerritoireView)
router.register('chefferies', ChefferieView)
router.register('groupements', GroupementView)
router.register('villages', VillageView)

# action arg
actions = {'get': 'list', 'put': 'update', 'patch': 'update'}

urlpatterns = [
    # ALL-USERS
    path('', include(router.urls)),
    path('auth/', include("rest_framework.urls")), # route /api/auth/login
    path('auth/register', UserCreateView.as_view(), name='sign_up'),
    # Authentication required
    path('profiles/my-profile', UserProfileView.as_view(actions)),
    path('lots/upload', LotListCreateView.as_view(), name='upload_lots'),
    path('lots/stats/current-user', current_user_lots, name='lots_stats'),
    path('lots/details', LotModelView.as_view(actions), name='lots_details'),
    path('lots/hyperlinks', LotHyperlinkedView.as_view(actions), name='lots_hyperlinks'),
]