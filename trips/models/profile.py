from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from trips.utils.enums import UserRole

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	role = models.CharField(max_length=100, choices=UserRole.choices, default=UserRole.USER)
	
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
		return self.user.get_full_name() or self.user.username
	

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()
	
	
	
	
	
	