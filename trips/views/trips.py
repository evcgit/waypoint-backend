from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from trips.models import Trip
from trips.serializers import TripSerializer, TripCreateUpdateSerializer

class TripViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TripSerializer
    
    def get_queryset(self):
        user_profile = self.request.user.profile
        return Trip.objects.filter(
            Q(owner=user_profile) | 
            Q(travelers=user_profile)
        ).distinct().order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TripCreateUpdateSerializer
        return TripSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile)
    
    @action(detail=False, methods=['get'])
    def owned(self):
        """Get only trips owned by the user"""
        trips = Trip.objects.filter(owner=self.request.user.profile)
        serializer = self.get_serializer(trips, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def participating(self):
        """Get trips where user is a traveler but not owner"""
        trips = Trip.objects.filter(
            travelers=self.request.user.profile
        ).exclude(owner=self.request.user.profile)
        serializer = self.get_serializer(trips, many=True)
        return Response(serializer.data) 
    