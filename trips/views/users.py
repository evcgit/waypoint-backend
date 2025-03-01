from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import CreateAPIView
from trips.serializers.users import UserSerializer, ProfileSerializer
from django.contrib.auth.models import User
from trips.models.profile import Profile

class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Optionally, you can implement logic to blacklist the refresh token here
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RetrieveUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)