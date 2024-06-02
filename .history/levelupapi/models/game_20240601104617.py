from django.db import models
from .game_type import Game_Type
from .gamer import Gamer


class Game(models.Model):
    title = models.CharField(max_length=50)
    maker = models.CharField(max_length=50)
    number_of_players = models.CharField(max_length=50)
    skill_level = models.IntegerField()
    game_type = models.ForeignKey(Game_Type, on_delete=models.CASCADE)
    gamer = models.ForeignKey(Gamer, on_delete=models.CASCADE)
