from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event


class EventView(ViewSet):
    """Level up event types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event type

        Returns:
            Response -- JSON serialized event type
        """
        event = Event.objects.get(pk=pk)
        serializer = GameViewSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all event types

        Returns:
            Response -- JSON serialized list of event types
        """
        event = Event.objects.all()
        serializer = GameViewSerializer(event, many=True)
        return Response(serializer.data)

class GameViewSerializer(serializers.ModelSerializer):
    """JSON serializer for event types
    """
    class Meta:
        model = Event
        fields = ('id', 'game_type', 'title', 'maker', 'number_of_players', 'skill_level')
