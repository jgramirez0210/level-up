from django.db import models


class Game_Type(models.Model):

    uid = models.CharField(max_length=50)
    bio = models.CharField(max_length=50)
