from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from trips.serializers.users import UserSerializer
from django.contrib.auth.models import User
from trips.models.profile import Profile
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
        
        for field, value in data.items():
            if isinstance(value, dict) and 'id' in value:
                data[field] = value['id']
            
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        return Response(self.get_serializer(request.user).data)
    
    @action(detail=False, methods=['post'])
    def logout(self, request, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)


			
			
