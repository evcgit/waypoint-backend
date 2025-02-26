from rest_framework.routers import DefaultRouter
from django.urls import path, include
from trips.views import TripViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from trips.views.users import UserRegistrationView, LogoutView


router = DefaultRouter()
router.register(r'trips', TripViewSet, basename='trip')

urlpatterns = [
    path('', include(router.urls)),
		path('register/', UserRegistrationView.as_view(), name='user_registration'),  # User registration
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtain token
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
    path('auth/logout/', LogoutView.as_view(), name='logout'),  # Logout
] 