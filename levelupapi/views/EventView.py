from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.http import HttpResponseServerError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game, EventGamer
from rest_framework.decorators import action
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

class EventView(viewsets.ModelViewSet):
    """Level up event types view"""
    queryset = Event.objects.all()

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
        uid = request.META['HTTP_AUTHORIZATION']
        gamer = Gamer.objects.get(uid=uid)
         
        for event in events:
            event.joined = len(EventGamer.objects.filter(gamer=gamer, event=event)) > 0

        serializer = EventViewSerializer(events, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized event instance
        """
        gamer = None 
        game = Game.objects.get(pk=request.data["gameId"])
        uid = request.data["userId"]

        organizer = Gamer.objects.get(uid=uid)

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


    @action(methods=['post', 'put'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
        
        gamer = Gamer.objects.get(uid=request.data["userId"])
        event = Event.objects.get(pk=pk)
        attendee = EventGamer.objects.create(
            gamer=gamer,
            event=event
        )
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Handle DELETE requests to leave an event"""
        # Check if 'userId' is in request.data
        if 'userId' not in request.data:
            return Response({'message': 'userId is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            gamer = Gamer.objects.get(uid=request.data["userId"])
            event = Event.objects.get(pk=pk)

            attendee = EventGamer.objects.get(gamer=gamer, event=event)
            attendee.delete()

            return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)
        except Gamer.DoesNotExist:
            return Response({'message': 'Gamer does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Event.DoesNotExist:
            return Response({'message': 'Event does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except EventGamer.DoesNotExist:
            return Response({'message': 'Gamer is not registered for this event.'}, status=status.HTTP_404_NOT_FOUND)
class EventViewSerializer(serializers.ModelSerializer):
    """JSON serializer for event types"""
    class Meta:
        model = Event
        fields = ['id', 'game', 'organizer', 'description', 'date', 'time', 'joined']