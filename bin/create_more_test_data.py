from trips.models.trips import Trip, Destination, Accommodation, Activity, Transport
from datetime import datetime, timedelta
import pytz

def create_trip_details(trip, start_date):
    # Create 3 destinations for the trip
    destinations = []
    current_date = start_date
    
    # Different cities based on trip title
    if "Europe" in trip.title:
        cities = [("Paris", "France"), ("Rome", "Italy"), ("Barcelona", "Spain")]
    elif "South Africa" in trip.title:
        cities = [("Cape Town", "South Africa"), ("Johannesburg", "South Africa"), ("Durban", "South Africa")]
    elif "Puerto Rico" in trip.title:
        cities = [("San Juan", "Puerto Rico"), ("Ponce", "Puerto Rico"), ("Fajardo", "Puerto Rico")]
    elif "Japan" in trip.title:
        cities = [("Tokyo", "Japan"), ("Kyoto", "Japan"), ("Osaka", "Japan")]
    
    # Create destinations
    for i, (city, country) in enumerate(cities):
        destination = Destination.objects.create(
            trip=trip,
            city=city,
            country=country,
            arrival_date=current_date,
            departure_date=current_date + timedelta(days=4),
            notes=f"Exploring {city}",
            order=i
        )
        destinations.append(destination)
        current_date += timedelta(days=4)

        # Create accommodation for each destination
        checkin_time = datetime.combine(destination.arrival_date, datetime.min.time().replace(hour=14))
        checkout_time = datetime.combine(destination.departure_date, datetime.min.time().replace(hour=11))
        Accommodation.objects.create(
            destination=destination,
            name=f"{city} Hotel",
            checkin_date=pytz.UTC.localize(checkin_time),
            checkout_date=pytz.UTC.localize(checkout_time),
            notes="Central location",
            cost=150.00
        )

        # Create 2 activities for each destination
        activity_start = pytz.UTC.localize(datetime.combine(destination.arrival_date, datetime.min.time().replace(hour=10)))
        for j in range(2):
            Activity.objects.create(
                destination=destination,
                name=f"Activity {j+1} in {city}",
                start_time=activity_start + timedelta(days=j),
                end_time=activity_start + timedelta(days=j, hours=3),
                notes=f"Exciting activity in {city}",
                cost=50.00
            )

    # Create transport between destinations
    for i in range(len(destinations) - 1):
        from_dest = destinations[i]
        to_dest = destinations[i + 1]
        departure_time = pytz.UTC.localize(datetime.combine(from_dest.departure_date, datetime.min.time().replace(hour=9)))
        Transport.objects.create(
            from_destination=from_dest,
            to_destination=to_dest,
            name=f"Transport from {from_dest.city} to {to_dest.city}",
            start_time=departure_time,
            end_time=departure_time + timedelta(hours=3),
            notes="Comfortable journey",
            cost=100.00
        )

# After creating each trip, add the details
trips = Trip.objects.all()
for trip in trips:
    create_trip_details(trip, trip.start_date)
    print(f"Added details to trip: {trip.title}")
    print(f"- Destinations: {trip.all_destinations.count()}")
    print(f"- Accommodations: {trip.all_accommodations.count()}")
    print(f"- Activities: {trip.all_activities.count()}")
    print(f"- Transport: {trip.all_transport.count()}")