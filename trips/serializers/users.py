from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from trips.models.profile import Profile
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    role = serializers.CharField(source='profile.role', read_only=True)
    phone = serializers.CharField(source='profile.phone', allow_blank=True)
    date_of_birth = serializers.DateField(source='profile.date_of_birth', allow_null=True)
    passport_expiry = serializers.DateField(source='profile.passport_expiry', allow_null=True)
    nationality = serializers.CharField(source='profile.nationality', allow_blank=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'password',
            'role', 'phone', 'date_of_birth', 'passport_expiry', 'nationality'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        
        # (profile is auto-created by signal)
        user = User.objects.create_user(**validated_data)
        for field, value in profile_data.items():
            setattr(user.profile, field, value)
        user.profile.save()

        return user

    def update(self, instance, validated_data):        
        if 'profile' in validated_data:
            profile_data = validated_data.pop('profile')
            for field, value in profile_data.items():
                setattr(instance.profile, field, value)
            instance.profile.save()

        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance

