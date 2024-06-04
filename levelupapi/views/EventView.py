from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game


class EventView(ViewSet):
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
        """Handle PUT requests for a event
    
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

      

class EventViewSerializer(serializers.ModelSerializer):
    """JSON serializer for event types
    """
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer')
