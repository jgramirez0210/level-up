# from django.http import HttpResponseServerError
# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response
# from rest_framework import serializers
# from levelupapi.models import Gamer

# class GamerView(ViewSet):
#     """Level up gamers view"""
    
#     def list(self, request):
#         """Handle GET requests to get all gamers """
#         queryset = Gamer.objects.all()

#         serializer = GamerSerializer(queryset, many=True)
#         return Response(serializer.data)

#     @classmethod
#     def get_extra_actions(cls):
#         return []
    
#     def create(self, request):
#         """Handle POST operations   

#         Returns
#             Response -- JSON serialized game instance
#         """
# class GamerSerializer(serializers.ModelSerializer):
#     """JSON serializer for gamers
#     """
#     class Meta:
#         model = Gamer
#         fields = ('id', 'bio')