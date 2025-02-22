from rest_framework import serializers
from trips.models import Trip, TripTraveler, Destination, Accommodation, Activity, Transport, Profile

class ProfileLightSerializer(serializers.ModelSerializer):
    """Light version of Profile serializer for nested relationships"""
    class Meta:
        model = Profile
        fields = ['id', 'user', 'phone']

class TripTravelerSerializer(serializers.ModelSerializer):
    traveler = ProfileLightSerializer(read_only=True)
    
    class Meta:
        model = TripTraveler
        fields = ['id', 'traveler', 'role', 'created_at']

class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = ['id', 'name', 'checkin_date', 'checkout_date', 'notes', 
                 'created_at', 'updated_at', 'cost', 'duration']
        read_only_fields = ['created_at', 'updated_at', 'duration']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'name', 'start_time', 'end_time', 'notes', 
                 'created_at', 'updated_at', 'cost', 'duration']
        read_only_fields = ['created_at', 'updated_at', 'duration']

class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = ['id', 'name', 'from_destination', 'to_destination',
                 'start_time', 'end_time', 'notes', 'created_at', 
                 'updated_at', 'cost', 'duration', 'is_local']
        read_only_fields = ['created_at', 'updated_at', 'duration', 'is_local']

class DestinationSerializer(serializers.ModelSerializer):
    accommodations = AccommodationSerializer(source='accommodation_set', many=True, read_only=True)
    activities = ActivitySerializer(source='activity_set', many=True, read_only=True)
    transports_from = TransportSerializer(many=True, read_only=True)
    transports_to = TransportSerializer(many=True, read_only=True)
    
    class Meta:
        model = Destination
        fields = ['id', 'city', 'country', 'arrival_date', 'departure_date',
                 'notes', 'created_at', 'updated_at', 'order', 'total_expenses',
                 'duration', 'accommodations', 'activities', 'transports_from',
                 'transports_to']
        read_only_fields = ['created_at', 'updated_at', 'total_expenses', 'duration']

class TripSerializer(serializers.ModelSerializer):
    travelers = TripTravelerSerializer(source='triptraveler_set', many=True, read_only=True)
    destinations = DestinationSerializer(source='destination_set', many=True, read_only=True)
    owner = ProfileLightSerializer(read_only=True)
    
    class Meta:
        model = Trip
        fields = ['id', 'title', 'notes', 'start_date', 'end_date', 
                 'created_at', 'updated_at', 'owner', 'travelers',
                 'status', 'budget', 'currency', 'visa_required',
                 'visa_link', 'destinations', 'total_expenses',
                 'total_duration']
        read_only_fields = ['created_at', 'updated_at', 'total_expenses',
                           'total_duration']

class TripCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'title', 'notes', 'start_date', 'end_date',
                 'status', 'budget', 'currency', 'visa_required',
                 'visa_link'] 