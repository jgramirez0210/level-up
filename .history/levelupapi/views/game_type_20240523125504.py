"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game_Type, Game


class GameTypeView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        game_type = Game_Type.objects.get(pk=pk)
        serializer = GameTypeSerializer(game_type)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all games
    
        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()
    
        # Add in the next 3 lines
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)
    
        serializer = GameTypeSerializer(games, many=True)
        return Response(serializer.data)

class GameTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game_Type
        fields = ('id', 'label')
