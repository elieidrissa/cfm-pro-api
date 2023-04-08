from django.urls import path, include, re_path
from rest_framework import routers
from .views import *
# JWT authentication
from rest_framework_simplejwt.views import (TokenObtainPairView, 
                                            TokenRefreshView)
# documentation
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# profiles pics 
from django.conf import settings
from django.conf.urls.static import static

# SWAGGER
schema_view = get_schema_view(
   openapi.Info(
      title="CFM PRO API",
      default_version='v1',
      description="This api serves as backend to all CFM Pro projets",
      terms_of_service="https://www.cfm-pro.com/policies-and-terms/",
      contact=openapi.Contact(email="sowerbean@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

# ROUTING
router  = routers.DefaultRouter()
# lots
router.register('lots', LotCustomView)
router.register('lots/hyperlinks', LotHyperlinkedView) #coord only
router.register('lots/keys', LotModelView) #coord only
# users
router.register('users', UserRetrieveListView) #write_only
router.register('zones', UserZoneListView) #read_only
router.register('perimetres', UserPerimetreListView) #read_only
router.register('profiles', UserProfileListView)
# additional data
router.register('negociants', NegociantView)
router.register('transporteurs', TransporteurView)
router.register('minerais', MineraiView)
router.register('cooperatives', CooperativeView)
router.register('axes', AxeView)
router.register('sites', SiteView)
router.register('chantiers', ChantierView)
# province, territoires - data / Read Only
router.register('provinces', ProvinceView)
router.register('territoires', TerritoireView)
router.register('chefferies', ChefferieView)
router.register('groupements', GroupementView)
router.register('villages', VillageView)

# this is needed by views ohter than ModelViewset/ I don't know why
actions = {'get': 'list', 'put': 'update', 'patch': 'update'}

urlpatterns = [
    # ALL-USERS 
    path('', include(router.urls)),
    path('auth/token/', TokenObtainPairView.as_view()), #JWT / get tokens
    path('auth/token/refresh/', TokenRefreshView.as_view()), #JWT/ renew tokens
    path('auth/', include("rest_framework.urls")), # route /api/v1/auth/login
    path('auth/register/', UserCreateView.as_view()),

    # Authentication required
    path('auth/my-profile', UserProfileView.as_view(actions)),
    path('lots/upload', LotListCreateView.as_view()),

    # FILTERS / only COORD and higher are allowed
    path('filter/lots', LotFilterListView.as_view()),
    path('filter/negociants', NegociantFilterListView.as_view()),
    path('filter/transporteurs', TransporteurFilterListView.as_view()),
    path('filter/minerais', MineraiFilterListView.as_view()),
    path('filter/chantiers', ChantierFilterListView.as_view()),
    path('filter/sites', SiteFilterListView.as_view()),
    
    # address filters / open to every authenticated user
    path('filter/territoires', TerritoireFilterListView.as_view()),
    path('filter/chefferies', ChefferieFilterListView.as_view()),
    path('filter/groupements', GroupementFilterListView.as_view()),
    path('filter/villages', VillageFilterListView.as_view()),

    # DOCUMENTATION / SwaggerUI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


