from django.db import models
import uuid

class Country(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=200)
	alpha2 = models.CharField(max_length=2)
	alpha3 = models.CharField(max_length=3)
	numeric = models.CharField(max_length=3)
	last_updated = models.DateTimeField(auto_now=True)

	