from django.db import models

# Create your models here.

class roomInfo(models.Model):
    roomID = models.AutoField(primary_key=True, auto_created=True)
    roomName = models.CharField(max_length=50)
    roomDescription = models.CharField(max_length=200)
    roomCapacity = models.IntegerField()

class facilities(models.Model):
    facilityID = models.AutoField(primary_key=True, auto_created=True)
    facilityName = models.CharField(max_length=50)
    facilityDescription = models.CharField(max_length=200)

class roomFacilities(models.Model):
    roomFacilitiesID = models.AutoField(primary_key=True, auto_created=True)
    roomID = models.ForeignKey(roomInfo)
    facilityID = models.ForeignKey(facilities)

class periods(models.Model):
    periodID = models.AutoField(primary_key=True, auto_created=True)
    periodName = models.CharField(max_length=50)
    startTime = models.TimeField(auto_now=False)
    endTime = models.TimeField(auto_now=False)

class roomAvailability(models.Model):
    roomAvailabilityID = models.AutoField(primary_key=True, auto_created=True)
    date = models.DateField(auto_now=False)
    periodID = models.ForeignKey(periods)

class bookingRecord(models.Model):
    bookingRecordID = models.AutoField(primary_key=True, auto_created=True)
    date = models.DateField(auto_now=False)
    periodID = models.ForeignKey(periods)
    roomID = models.ForeignKey(roomInfo)

class bookingHistory(models.Model):
    bookingHistoryID = models.AutoField(primary_key=True, auto_created=True)
    date = models.DateField(auto_now=False)
    periodID = models.ForeignKey(periods)
    roomID = models.ForeignKey(roomInfo)
    timestamp = models.TimeField(auto_now_add=True)
