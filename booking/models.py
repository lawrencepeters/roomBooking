from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Room(models.Model):
    roomID = models.AutoField(primary_key=True, auto_created=True)
    roomName = models.CharField(max_length=50)
    roomDescription = models.CharField(max_length=200)
    roomCapacity = models.IntegerField()

    def __str__(self):
        return '%s - %s' % (self.roomName, self.roomDescription)

class Facility(models.Model):
    facilityID = models.AutoField(primary_key=True, auto_created=True)
    facilityName = models.CharField(max_length=50)
    facilityDescription = models.CharField(max_length=200)
    
    def __str__(self):
        return '%s - %s' % (self.facilityName, self.facilityDescription)

class RoomFacility(models.Model):
    roomFacilitiesID = models.AutoField(primary_key=True, auto_created=True)
    room = models.ForeignKey(Room)
    facility = models.ForeignKey(Facility)

    def __str__(self):
        return '%s - %s' % (self.room.roomName, self.facility.facilityName)

class Period(models.Model):
    periodID = models.AutoField(primary_key=True, auto_created=True)
    periodName = models.CharField(max_length=50)
    startTime = models.TimeField(auto_now=False)
    endTime = models.TimeField(auto_now=False)

    def __str__(self):
        return self.periodName

class Booking(models.Model):
    bookingID = models.AutoField(primary_key=True, auto_created=True)
    date = models.DateField(auto_now=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    period = models.ForeignKey(Period)
    room = models.ForeignKey(Room)
    timestamp = models.TimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s - %s - %s' % (self.date, self.user.username, self.period.periodName, self.room.roomName)

class BookingHistory(models.Model):
    bookingHistoryID = models.AutoField(primary_key=True, auto_created=True)
    date = models.DateField(auto_now=False)
    user = User
    period = Period
    room = Room
    timestamp = models.TimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s - %s - %s - %s' % (self.date, self.user.username, self.period.periodName, self.room.roomName, self.timestamp)
