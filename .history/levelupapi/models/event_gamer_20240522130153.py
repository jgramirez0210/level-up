from django.db import models
from .type import Type


class Event_Gamer(models.Model):

    gamer = models.ForeignKey(Type, on_delete=models.CASCADE)
    event = models.CharField(max_length=50)
