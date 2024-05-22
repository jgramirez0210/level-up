from django.db import models
from .game_type import Game_Type


class Game_Type(models.Model):
    game_type = models.ForeignKey(Game_Type, on_delete=models.CASCADE)
    label = models.CharField(max_length=50)
