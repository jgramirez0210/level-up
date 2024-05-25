from django.db import models
from .gamer import Gamer
from .event import Event
from .game_type import Game_Type

class EventGamer(models.Model):
  gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
  event = models.ForeignKey(Event, on_delete=models.CASCADE)
  game_type = models.ForeignKey(Game_Type, on_delete=models.CASCADE)
