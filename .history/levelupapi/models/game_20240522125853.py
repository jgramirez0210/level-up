from django.db import models
from .type import Type


class Game(models.Model):

    game_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    maker = models.CharField(max_length=50)
    gamer = models.ForeignKey(Type, on_delete=models.CASCADE)
    number_of_players = models.CharField(max_length=50)
    skill_level = models.CharField(max_length=50)
