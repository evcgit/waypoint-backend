from django.db import models

class TripStatus(models.TextChoices):
    PLANNING = 'PLANNING'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    
    

class UserRole(models.TextChoices):
    ADMIN = 'ADMIN'
    USER = 'USER'
    GUEST = 'GUEST'
    
    
