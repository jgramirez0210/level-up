from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from levelupapi.models import Event, Gamer, Game
from levelupapi.views.EventView import EventViewSerializer
from django.test import TestCase
from levelupapi.models import Event
from django.utils import timezone
from datetime import datetime

class EventTests(APITestCase):
    fixtures = ['gamers', 'game_types', 'events', 'games']
  
    def setUp(self):
        # Create and save a Gamer instance before creating an Event
        gamer = Gamer.objects.create()  # Assuming Gamer model has an 'id' field
        # Ensure a Game instance exists and use its id for the event
        if not Game.objects.exists():
            game = Game.objects.create(name="Test Game", game_type_id=1, number_of_players=4, gamer=gamer)
        else:
            game = Game.objects.first()
        self.event = Event.objects.create(description="Test Event", organizer=gamer, date=timezone.now(), time=timezone.now(), game=game)
    
    def test_create_event(self):
        """Create event test"""
        url = "/events"
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        # Assuming the organizer_id and game_id are correctly set up in the fixtures or setUp method
        event_payload = {
            "description": "Another Test Event",
            "date": current_date,
            "time": current_time, 
            "game_id": self.event.game.id,  # Use the game id from the setup
            "organizer_id": self.event.organizer.id,  # Use the organizer id from the setup
        }
        response = self.client.post(url, event_payload, format='json')
    
        # Assertions remain the same
    
        # Get the last event added to the database, it should be the one just created
        new_event = Event.objects.last()
        expected = EventViewSerializer(new_event)
        self.assertEqual(expected.data, response.data)
        
    def test_change_event(self):
        """test update event"""
        # Ensure an event exists to update; create one if necessary
        if not Event.objects.exists():
            Event.objects.create(description="Initial Event", date="2023-01-01", time="12:00:00", game_id=1, organizer_id=1)
        
        event = Event.objects.first()  # Get the first event to update
        url = f'/events/{event.id}/'  # Ensure the URL is correct
        
        # Update event payload
        updated_event = {
            "description": "Updated Test Event",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "game_id": 1,
            "organizer_id": 1,
        }
        
        # Attempt to update the event
        response = self.client.put(url, updated_event, format='json')
        
        # Check if the update was successful
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code, "Expected 204 status code after updating event")
        
        # Refresh and serialize the updated event for comparison
        event.refresh_from_db()
        expected = EventViewSerializer(event).data
        
        # Fetch the updated event directly to compare
        response = self.client.get(url, format='json')
        self.assertEqual(expected, response.data, "Updated event data does not match expected data")
        
    def test_get_event(self):
        """Get event Test"""
        if not Event.objects.filter(id=1).exists():
            self.fail("Event with ID 1 does not exist.")

        url = "/events/1/"

        response = self.client.get(url, format='json')

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND, "Event not found.")

        event = Event.objects.get(id=1)
        expected = EventViewSerializer(event)

        self.assertEqual(expected.data, response.data)

    def test_list_events(self):
        """Test list events"""
        url = '/events'
        response = self.client.get(url)

        all_events = Event.objects.all()
        expected = EventViewSerializer(all_events, many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)    

