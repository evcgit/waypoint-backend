from rest_framework.routers import DefaultRouter
from django.urls import path, include
from trips.views import TripViewSet

router = DefaultRouter()
router.register(r'trips', TripViewSet, basename='trip')

urlpatterns = [
    path('', include(router.urls)),
] 