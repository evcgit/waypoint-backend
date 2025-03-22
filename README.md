# Waypoint Backend


Things to do:
- Models:
Add an address field to trip sub-models
Figure out how we want to store files for a trip(which model are they related to?)


- Serializers:
Simplify the TripSerializer to not return all details for sub-models in a single trip view

- Views:
Add a way to add/update/delete an accommodation to a trip
Add a way to add/update/delete an activity to a trip
Add a way to add/update/delete a transport to a trip
Add a way to add/update/delete a destination to a trip
Add a way to add/update/delete a traveler to a trip
Handle crud permissions based on the role of the user for that trip (admin, traveler, owner)
Automatically update trip status based on the date of the trip




API:
- Implement api call to get visa requirements for a trip - API found
- Implement api call to get weather for a trip and provide summary or suggestions of clothing/packing
- Implement api call to get flight options for a trip? - Needed for an explore/favorites page
- Implement api call to get hotel options for a trip? - Needed for an explore/favorites page
- Implement api call to get activity options for a trip? - Needed for an explore/favorites page
- Implement api call to get transport options for a trip? - Needed for an explore/favorites page


- Ideas:
View for tracking expenses
View for everyone going on the trip to vote on trip sub-models
Find a way to make it easy for users to save their confirmations emails/etc. for a trip(something better than inputs)
Create accounts using google/apple id