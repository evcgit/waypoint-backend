from rest_framework import serializers
from trips.models import Country

class CountrySerializer(serializers.ModelSerializer):
	id = serializers.UUIDField(read_only=True)
	class Meta:
		model = Country
		fields = ['id', 'name', 'alpha2']