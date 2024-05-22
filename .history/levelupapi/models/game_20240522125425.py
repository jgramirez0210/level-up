from django.db import models


class Gamer(models.Model):

    label = models.CharField(max_length=50)
