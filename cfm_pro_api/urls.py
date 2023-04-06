from django.urls import path, include
from rest_framework import routers
from .views import *

router  = routers.DefaultRouter()
# lots
router.register('lots', LotCustomView)
router.register('lots/hyperlinks', LotHyperlinkedView) #coord only
router.register('lots/keys', LotModelView) #coord only
# users
router.register('users', UserRetrieveListView) #write_only
router.register('zones', UserZoneListView) #read_only
router.register('profiles', UserProfileListView)
# additional data
router.register('negociants', NegociantView)
router.register('transporteurs', TransporteurView)
router.register('minerais', MineraiView)
router.register('coopratives', CooperativeView)
router.register('axes', AxeView)
router.register('sites', SiteView)
router.register('chantiers', ChantierView)
# province, territoires - data / Read Only
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
    path('auth/', include("rest_framework.urls")), # route /api/v1/auth/login
    path('auth/register', UserCreateView.as_view()),
    # path('zones/', UserZoneListView.as_view(actions)),
    # Authentication required
    path('user/profile', UserProfileView.as_view(actions)),
    path('lots/upload', LotListCreateView.as_view()),

    # FILTERS / only COORD and higher are allowed
    path('filter/lots', LotFilterListView.as_view()),
    path('filter/negociants', NegociantFilterListView.as_view()),
    path('filter/transporteurs', TransporteurFilterListView.as_view()),
    path('filter/minerais', MineraiFilterListView.as_view()),
    path('filter/chantiers', ChantierFilterListView.as_view()),
    path('filter/sites', SiteFilterListView.as_view()),
    # address filters
    path('filter/territoires', TerritoireFilterListView.as_view()),
    path('filter/chefferies', ChefferieFilterListView.as_view()),
    path('filter/groupements', GroupementFilterListView.as_view()),
    path('filter/villages', VillageFilterListView.as_view()),
]