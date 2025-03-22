from rest_framework import viewsets, permissions
from rest_framework.response import Response
from trips.models import Country
from trips.serializers import CountrySerializer

class CountryViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = CountrySerializer
	queryset = Country.objects.all()

	def list(self, request):
		countries = Country.objects.all()
		serializer = self.get_serializer(countries, many=True)
		return Response(serializer.data)