#Import default django  modules
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

#Decleration of model for databse

class Room(models.Model):
    roomID = models.AutoField(primary_key=True, auto_created=True)  #Primary Key
    roomName = models.CharField(max_length=50)  #Character field
    roomDescription = models.CharField(max_length=200)  #Character field
    roomCapacity = models.IntegerField()    #Integer field

    #Changes default object display in admin view
    def __str__(self):
        return '%s - %s' % (self.roomName, self.roomDescription)    

class Facility(models.Model):
    facilityID = models.AutoField(primary_key=True, auto_created=True)  #Primary Key
    facilityName = models.CharField(max_length=50)  #Character field
    facilityDescription = models.CharField(max_length=200)  #Character field

    #Changes the default name in the admin view
    class Meta:
        verbose_name='Facility'
        verbose_name_plural='Facilities'
    
    #Changes default object display in admin view 
    def __str__(self):
        return '%s - %s' % (self.facilityName, self.facilityDescription)

class RoomFacility(models.Model):
    roomFacilitiesID = models.AutoField(primary_key=True, auto_created=True)    #Primary Key
    room = models.ForeignKey(Room)  #Foreign key
    facility = models.ForeignKey(Facility)  #Foreign key

    #Changes the default name in the admin view
    class Meta:
        verbose_name='Room Facility'
        verbose_name_plural='Room Facilities'

    #Changes default object display in admin view
    def __str__(self):
        return '%s - %s' % (self.room.roomName, self.facility.facilityName)

class Period(models.Model):
    periodID = models.AutoField(primary_key=True, auto_created=True)    #Primary Key
    periodName = models.CharField(max_length=50)    #Character field
    startTime = models.TimeField(auto_now=False)    #Time field
    endTime = models.TimeField(auto_now=False)  #Time field

    #Changes default object display in admin view
    def __str__(self):
        return self.periodName

class Booking(models.Model):
    bookingID = models.AutoField(primary_key=True, auto_created=True)   #Primary Key
    date = models.DateField(auto_now=False) #Date field
    user = models.ForeignKey(settings.AUTH_USER_MODEL)  #Foreign key
    period = models.ForeignKey(Period)  #Foreign key
    room = models.ForeignKey(Room)  #Foreign key
    timestamp = models.DateTimeField(auto_now_add=True) #Date-time field

    #Changes default object display in admin view
    def __str__(self):
        return '%s - %s - %s - %s' % (self.date, self.user.username, self.period.periodName, self.room.roomName)

class BookingHistory(models.Model):
    bookingHistoryID = models.AutoField(primary_key=True, auto_created=True)    #Primary Key
    date = models.DateField(auto_now=False)
    username = models.CharField(max_length=50, null = True) #Character field
    periodName = models.CharField(max_length=50, null = True)   #Character field
    roomName = models.CharField(max_length=50, null = True) #Character field
    timestamp = models.DateTimeField(auto_now_add=True) #Date-time field

    #Changes the default name in the admin view
    class Meta:
        verbose_name='Booking History'
        verbose_name_plural='Booking History'

    #Changes default object display in admin view
    def __str__(self):
        return '%s - %s - %s - %s - %s' % (self.date, self.username, self.periodName, self.roomName, self.timestamp)
