from django.shortcuts import render
import datetime
import pprint

# Create your views here.

from .models import roomInfo, facilities, roomFacilities, periods, roomAvailability, bookingRecord, bookingHistory
def index(request):
    """
    View function for home page of site.
    """
    room  = roomInfo.objects.all()
    period  = periods.objects.all()
    # Generate counts of some of the main objects
    # num_roomAvailabilities=roomAvailability.objects.all().count()
    # Available books (status = 'a')
    # num_rooms_available=roomAvailability.objects.filter(status__exact='a').count()
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'rooms':room, 'periods':period},
    ) 

def viewbookings(request):
    room  = roomInfo.objects.all()
    period  = periods.objects.all()

    return render(
        request,
        'viewbookings.html',
        context={'rooms':room, 'periods':period},
    ) 

def find(request):

    bookingDate = datetime.datetime.strptime(request.POST['bookingdate'], "%d/%m/%Y").strftime("%Y-%m-%d")

    bookedRooms = bookingRecord.objects.filter(date = bookingDate).values('roomID')

    pprint.pprint(bookedRooms)

    selectedRooms = roomInfo.objects.exclude(roomID__in=[o['roomID'] for o in bookedRooms])
    #for room in selectedRooms:
        #if booking is not None:
        #   selectedRooms.exclude(room)

    return render(
        request,
        'find.html',
        context={'bookingDates': bookingDate, 'selectedRooms': selectedRooms},
    ) 