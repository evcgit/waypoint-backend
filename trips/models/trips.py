from django.db import models
from .profile import Profile
from datetime import timedelta
import uuid
from trips.utils.enums import TripStatus

class Trip(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owned_trips', null=True, blank=True)
    travelers = models.ManyToManyField(
        Profile, 
        through='TripTraveler',
        related_name='trips_participating'
    )
    status = models.CharField(max_length=20, choices=TripStatus.choices, default=TripStatus.PLANNING)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    visa_required = models.BooleanField(default=False)
    visa_link = models.URLField(blank=True)
    
    
    @property
    def all_destinations(self):
        return Destination.objects.filter(trip=self)
    
    @property
    def all_accommodations(self):
        return Accommodation.objects.filter(destination__trip=self)

    @property
    def all_activities(self):
        return Activity.objects.filter(destination__trip=self)

    @property
    def all_transports(self):
        return Transport.objects.filter(
            models.Q(from_destination__trip=self) | 
            models.Q(to_destination__trip=self)
        ).distinct()
    
    @property
    def all_travelers(self):
        return TripTraveler.objects.filter(trip=self).values_list('traveler', flat=True)

    @property
    def total_expenses(self):
        return sum(destination.total_expenses for destination in self.all_destinations)
    
    @property
    def total_duration(self):
        return sum((destination.duration for destination in self.all_destinations), timedelta())

    def __str__(self):
        return self.title

class TripTraveler(models.Model):
    ROLES = [
        ('ADMIN', 'Administrator'),
        ('TRAVELER', 'Traveler'),
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    traveler = models.ForeignKey(Profile, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES, default='TRAVELER')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['trip', 'traveler']

    def __str__(self):
        return f"{self.traveler.name} - {self.get_role_display()} on {self.trip.title}" 
        
class Destination(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'arrival_date']
    
    @property
    def total_expenses(self):
        accommodation_costs = sum(acc.cost for acc in self.accommodation_set.all())
        activity_costs = sum(act.cost for act in self.activity_set.all())
        transport_costs = sum(trans.cost for trans in self.transports_from.all())
        return accommodation_costs + activity_costs + transport_costs
    
    @property
    def duration(self):
        return self.departure_date - self.arrival_date

class Accommodation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    checkin_date = models.DateTimeField()
    checkout_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    @property
    def duration(self):
        return self.checkout_date - self.checkin_date

class Activity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    @property
    def duration(self):
        return self.end_time - self.start_time

class Transport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='transports_from')
    to_destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='transports_to')
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    @property
    def is_local(self):
        return self.to_destination is None
    
    @property
    def duration(self):
        return self.end_time - self.start_time
    