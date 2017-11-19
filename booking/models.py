# Create your models here.

from django.db import models


class Room(models.Model):
    roomName = models.CharField(max_length=50)
    roomDescription = models.CharField(max_length=200)
    roomCapacity = models.IntegerField()
