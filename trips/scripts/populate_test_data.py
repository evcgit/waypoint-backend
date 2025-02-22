from django.contrib.auth.models import User
from trips.models import Profile, Trip, TripTraveler, Destination, Accommodation, Activity, Transport
from django.utils import timezone
from datetime import timedelta, datetime
import random

# Create main user and profile
def create_test_data():
    # Create main user
    main_user = User.objects.create_user(
        username='main_user',
        email='main@example.com',
        password='password123'
    )
    main_profile = Profile.objects.create(
        user=main_user,
        phone='+1234567890',
        date_of_birth=datetime(1990, 1, 1),
        passport_expiry=datetime(2025, 1, 1),
        nationality='USA'
    )

    # Create additional users for travelers
    additional_profiles = []
    for i in range(5):
        user = User.objects.create_user(
            username=f'traveler{i}',
            email=f'traveler{i}@example.com',
            password='password123'
        )
        profile = Profile.objects.create(
            user=user,
            phone=f'+1234567{i}',
            date_of_birth=datetime(1990 + i, 1, 1),
            passport_expiry=datetime(2025, 1, 1),
            nationality=['USA', 'UK', 'Canada', 'Australia', 'France'][i]
        )
        additional_profiles.append(profile)

    # Create trips
    trips = []
    for i in range(3):
        start_date = timezone.now().date() + timedelta(days=30*i)
        trip = Trip.objects.create(
            title=f'Trip {i+1}',
            notes=f'Test trip {i+1} notes',
            start_date=start_date,
            end_date=start_date + timedelta(days=14),
            owner=main_profile,
            status=['PLANNING', 'IN_PROGRESS', 'COMPLETED'][i],
            budget=1000 * (i+1),
            currency='USD',
            visa_required=bool(i % 2),
            visa_link='https://example.com/visa' if i % 2 else ''
        )
        trips.append(trip)

        # Add travelers to trips
        for j, profile in enumerate(additional_profiles):
            if j % 2 == 0:  # Add some travelers, not all
                TripTraveler.objects.create(
                    trip=trip,
                    traveler=profile,
                    role='ADMIN' if j == 0 else 'TRAVELER'
                )

        # Create destinations for each trip
        for j in range(2):
            dest_start = start_date + timedelta(days=j*7)
            destination = Destination.objects.create(
                trip=trip,
                city=['Paris', 'London', 'Tokyo', 'New York'][j],
                country=['France', 'UK', 'Japan', 'USA'][j],
                arrival_date=dest_start,
                departure_date=dest_start + timedelta(days=6),
                notes=f'Destination {j+1} notes',
                order=j
            )

            # Create accommodations
            Accommodation.objects.create(
                destination=destination,
                name=f'Hotel {j+1}',
                checkin_date=timezone.make_aware(datetime.combine(dest_start, datetime.min.time())),
                checkout_date=timezone.make_aware(datetime.combine(dest_start + timedelta(days=6), datetime.min.time())),
                notes='Hotel notes',
                cost=200.00 * (j+1)
            )

            # Create activities
            for k in range(2):
                activity_start = timezone.make_aware(datetime.combine(dest_start + timedelta(days=k), datetime.min.time()))
                Activity.objects.create(
                    destination=destination,
                    name=f'Activity {k+1}',
                    start_time=activity_start,
                    end_time=activity_start + timedelta(hours=3),
                    notes='Activity notes',
                    cost=50.00 * (k+1)
                )

            # Create transport between destinations
            if j > 0:
                prev_destination = Destination.objects.filter(trip=trip).order_by('order')[j-1]
                Transport.objects.create(
                    from_destination=prev_destination,
                    to_destination=destination,
                    name=f'Flight {j}',
                    start_time=timezone.make_aware(datetime.combine(dest_start, datetime.min.time())),
                    end_time=timezone.make_aware(datetime.combine(dest_start + timedelta(hours=5), datetime.min.time())),
                    notes='Transport notes',
                    cost=300.00
                )

    print("Test data created successfully!")

# Run this in Django shell:
# from populate_test_data import create_test_data
# create_test_data()
