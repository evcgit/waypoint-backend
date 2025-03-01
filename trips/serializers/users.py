from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from trips.models.profile import Profile

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'phone_number', 'role']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
    
class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'role', 'date_of_birth', 'passport_expiry', 'nationality']
