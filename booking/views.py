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

    bookingDate = ''
    if 'bookDate' in request.GET:
        bookingDate = request.GET['bookDate']
        period = periods.objects.filter(periodID = request.GET['periodID']).get()
        room = roomInfo.objects.filter(roomID = request.GET['roomID']).get()
        b = bookingRecord(date = bookingDate, roomID = room, periodID = period)
        b.save()
    else:
        bookingDate = datetime.datetime.strptime(request.POST['bookingdate'], "%d/%m/%Y").strftime("%Y-%m-%d")
 
    bookedRooms = bookingRecord.objects.filter(date = bookingDate).values('roomID', 'periodID')

    displaydate = bookingDate[8:] + "/" + bookingDate[5:-3] + "/" + bookingDate[:4]

    allRooms = []
    for room in roomInfo.objects.all():
        allPeriods = []
        for period in periods.objects.all(): 
            isBooked = bookedRooms.filter(roomID = room).filter(periodID = period).count()
            allPeriods.append({"period": period, "isBooked": isBooked})
        allRooms.append({"room": room, "periods": allPeriods})

    pprint.pprint(allRooms)

    selectedRooms = roomInfo.objects.exclude(roomID__in=[o['roomID'] for o in bookedRooms])

    return render(
        request,
        'find.html',
        context={'bookingDate': bookingDate, 'allRooms': allRooms, 'periods': periods.objects.all(), 'displaydate': displaydate}
        ) 