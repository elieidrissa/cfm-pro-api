from django.urls import path, include
from rest_framework import routers
from .views import *

router  = routers.DefaultRouter()
# lots
router.register('lots', LotCustomView)
router.register('lots/hyperlinks', LotHyperlinkedView)
router.register('lots/keys', LotModelView)
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
    # Authentication required
    path('profiles/my-profile', UserProfileView.as_view(actions)),
    path('lots/upload', LotListCreateView.as_view()),

    # FILTERS / only COORD and higher are allowed
    path('filter/lots', LotFilterListView.as_view()),
    # path('filter/negociants', NegociantFilterListView.as_view()),
    # path('filter/transporteurs', TansporteurFilterListView.as_view()),
    # path('filter/chantiers', ChantierFilterListView.as_view()),
    # path('filter/sites', SiteListView.as_view()),
    # COORD
    path('lots/details', LotModelView.as_view(actions), name='lots_details'),
    path('lots/hyperlinks', LotHyperlinkedView.as_view(actions), name='lots_hyperlinks'),
    # Read Only
]