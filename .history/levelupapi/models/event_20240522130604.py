from django.db import models
from .game_type import Type


class Event(models.Model):

  game = models.ForeignKey(Type, on_delete=models.CASCADE)
  description = models.CharField(max_length=50)
  date = models.DateField()
  time = models.TimeField()
  organizer = models.ForeignKey(Type, on_delete=models.CASCADE)
    
