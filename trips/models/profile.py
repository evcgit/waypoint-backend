from django.contrib.auth.models import User
from django.db import models
import uuid

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	
	# Add travel-specific fields
	phone = models.CharField(max_length=20, blank=True)
	date_of_birth = models.DateField(null=True, blank=True)
	
	# Travel Documents
	passport_expiry = models.DateField(null=True, blank=True)
	nationality = models.CharField(max_length=100, blank=True)
	

	class Meta:
		verbose_name = 'Profile'
		verbose_name_plural = 'Profiles'

	def __str__(self):
		return self.get_full_name() or self.username
	
	
	
	
	
	