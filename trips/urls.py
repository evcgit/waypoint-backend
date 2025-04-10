from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TripViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views.users import UserViewSet
from .views.countries import CountryViewSet

router = DefaultRouter()
router.register(r'trips', TripViewSet, basename='trip')
router.register(r'users', UserViewSet, basename='user')
router.register(r'countries', CountryViewSet, basename='country')
urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtain token
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
]
