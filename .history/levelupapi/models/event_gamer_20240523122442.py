from django.db import models
from .game_type import Game_Type
from .gamer import Gamer
from .game import Game

class EventGamer(models.Model):

  game = models.ForeignKey(Game, on_delete=models.CASCADE)
  game_type = models.ForeignKey(Game_Type, on_delete=models.CASCADE)
  description = models.CharField(max_length=50)
  date = models.DateField()
  time = models.TimeField()
  organizer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
