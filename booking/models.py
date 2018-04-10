# Create your models here.

from django.db import models


class roomInfo(models.Model):
    roomID = models.AutoField(primary_key=True)
    roomName = models.CharField(max_length=50)
    roomDescription = models.CharField(max_length=200)
    roomCapacity = models.IntegerField()

class facilities(models.Model):
    facilityID = models.AutoField(primary_key=True)
    facilityName = models.CharField(max_length=50)
    facilityDescription = models.CharField(max_length=200)

class roomFacilities(models.Model):
    roomID = models.ForeignKey(roomInfo, primary_key=True)
    facilityID = models.ForeignKey(facilities)

class periods(models.Model):
    periodID = models.AutoField(primary_key=True)
    periodName = models.CharField(max_length=50)
    startTime = models.TimeField(auto_now=False)
    endTime = models.TimeField(auto_now=False)

class roomAvaliability(models.Model):
    date = models.DateField(auto_now=False)
    periodID = models.ForeignKey(periods)

class bookingRecord(models.Model):
    date = models.DateField(auto_now=False)
    periodID = models.ForeignKey(periods)

class bookingHistory(models.Model):
    date = models.DateField(auto_now=False)
    periodID = models.ForeignKey(periods)
    timestamp = models.TimeField(auto_now_add=True)
