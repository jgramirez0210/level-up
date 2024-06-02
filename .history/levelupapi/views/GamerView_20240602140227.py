from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game


class GamerView(ViewSet):
    """Level up event types view"""
    
    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        gamer = Gamer.objects.all()
        gamer = request.query_params.get('gamer', None)
        if gamer is not None:
            gamer = gamer.filter(game_id=gamer)

        serializer = EventViewSerializer(events, many=True)
        return Response(serializer.data)

class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
number_of_players = serializers.CharField()
skill_level = serializers.CharField()
class Meta:
    model = Game
    fields = ('id', 'bio')