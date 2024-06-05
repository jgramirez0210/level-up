from django.http import HttpResponseServerError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game, EventGamer
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


class EventView(viewsets.ModelViewSet):
    """Level up event types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event type
        Returns:
            Response -- JSON serialized event type
        """
        event = Event.objects.get(pk=pk)
        serializer = EventViewSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all events
        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()
        game_id = self.request.query_params.get('gameId', None)
        if game_id is not None:
            events = events.filter(game__id=game_id)
        serializer = EventViewSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized event instance
        """
        gamer = None 
        game = Game.objects.get(pk=request.data["gameId"])
        organizer = Gamer.objects.get(uid=request.data["userId"])

        event = Event.objects.create(
            game=game,
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            organizer=organizer
        )

        serializer = EventViewSerializer(event, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for an event
        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        print('data', request.data)  # print the request data
    
        organizer = Gamer.objects.get(id=request.data["userId"])
        event = Event.objects.get(pk=pk)
        attendee = EventGamer.objects.create(
            organizer=organizer,
            event=event,
            game_id=event.game_id,
            game_type_id=event.game.game_type_id,
            date=timezone.now(),
            time=timezone.now().time()
        )
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to leave an event"""

        organizer = Gamer.objects.get(id=request.data["userId"])
        event = Event.objects.get(pk=pk)
        attendee = EventGamer.objects.get(organizer=organizer, event=event)
        attendee.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
class EventViewSerializer(serializers.ModelSerializer):
    """JSON serializer for event types"""
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer')
        