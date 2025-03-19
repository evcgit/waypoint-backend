from django.contrib.auth.models import User
from trips.models import Trip
from trips.models.profile import Profile
from datetime import date, timedelta

# Create test users
test_users = [
    {
        'username': 'evan',
        'email': 'evan@example.com',
        'password': '1534',
        'first_name': 'Evan',
        'last_name': 'Cortez',
    },
    {
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'testpass123',
        'first_name': 'Bob',
        'last_name': 'Jones',
    },
    {
        'username': 'charlie',
        'email': 'charlie@example.com',
        'password': 'testpass123',
        'first_name': 'Charlie',
        'last_name': 'Brown',
    }
]

# Create users and get their profiles
profiles = []
for user_data in test_users:
    user = User.objects.create_user(**user_data)
    profile = user.profile
    profile.phone = '123-456-7890'
    profile.save()
    profiles.append(profile)

# Create a trip
trip = Trip.objects.create(
    title="Summer Europe Tour",
    notes="Amazing trip through Europe",
    start_date=date.today() + timedelta(days=30),
    end_date=date.today() + timedelta(days=44),
    owner=profiles[0],
    budget=5000.00,
    currency='EUR',
    visa_required=True,
    visa_link='https://example.com/visa'
)

trip = Trip.objects.create(
    title="Summer South Africa Tour",
    notes="Amazing trip through South Africa",
    start_date=date.today() + timedelta(days=30),
    end_date=date.today() + timedelta(days=44),
    owner=profiles[0],
    budget=5000.00,
    currency='EUR',
    visa_required=True,
    visa_link='https://example.com/visa'
)

trip = Trip.objects.create(
    title="Puerto Rico Trip",
    notes="Amazing trip through Puerto Rico",
    start_date=date.today() + timedelta(days=30),
    end_date=date.today() + timedelta(days=44),
    owner=profiles[0],
    budget=5000.00,
    currency='EUR',
    visa_required=True,
    visa_link='https://example.com/visa'
)

trip = Trip.objects.create(
    title="Japan Trip",
    notes="Amazing trip through Japan",
    start_date=date.today() + timedelta(days=30),
    end_date=date.today() + timedelta(days=44),
    owner=profiles[0],
    budget=5000.00,
    currency='EUR',
    visa_required=True,
    visa_link='https://example.com/visa'
)

# Add all profiles as travelers
trip.travelers.add(*profiles)

print("Created users:", ", ".join(u['username'] for u in test_users))
print(f"Created trip: {trip.title} with {trip.travelers.count()} travelers")