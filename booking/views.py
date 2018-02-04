from django.shortcuts import render
import datetime
import pprint
from django.contrib.auth.models import User

# Create your views here.

from .models import Room, Facility, RoomFacility, Period, Booking, BookingHistory
def index(request):
    """
    View function for home page of site.
    """
    rooms = Room.objects.all()
    periods = Period.objects.all()
    facilities = Facility.objects.all()
    
    return render(
        request,
        'index.html',
        context={'rooms':rooms, 'periods':periods, 'facilities':facilities},
    ) 

def viewbookings(request):
    rooms  = Room.objects.all()
    periods  = Period.objects.all()
    bookingDate = datetime.datetime.now().strftime("%Y-%m-%d")
    if request.method == 'POST':
        bookingDate = datetime.datetime.strptime(request.POST['bookDate'], "%d/%m/%Y").strftime("%Y-%m-%d")

    pprint.pprint(request.POST)

    bookedRooms = Booking.objects.filter(date = bookingDate).values('room', 'period')

    displaydate = bookingDate[8:] + "/" + bookingDate[5:-3] + "/" + bookingDate[:4]

    allRooms = []
    for room in Room.objects.all():
        allPeriods = []
        for period in Period.objects.all(): 
            isBooked = bookedRooms.filter(room = room).filter(period = period).count()
            allPeriods.append({"period": period, "isBooked": isBooked})
        allRooms.append({"room": room, "periods": allPeriods})

    return render(
        request,
        'viewbookings.html',
        context={'bookingDate': bookingDate,
                    'allRooms': allRooms,
                    'periods': Period.objects.all(),
                    'displaydate': displaydate},
    ) 

def find(request):

    bookingDate = ''
    if request.method == 'GET':
        bookingDate = request.GET['bookDate']
        period = Period.objects.filter(periodID = request.GET['periodID']).get()
        room = Room.objects.filter(roomID = request.GET['roomID']).get()
        b = Booking(date = bookingDate, room = room, period = period, user = request.user)
        b.save()
    else:
        bookingDate = datetime.datetime.strptime(request.POST['bookingdate'], "%d/%m/%Y").strftime("%Y-%m-%d")
 
    bookedRooms = Booking.objects.filter(date = bookingDate).values('room', 'period')

    displaydate = bookingDate[8:] + "/" + bookingDate[5:-3] + "/" + bookingDate[:4]

    allRooms = []
    for room in Room.objects.all():
        allPeriods = []
        for period in Period.objects.all(): 
            isBooked = bookedRooms.filter(room = room).filter(period = period).count()
            allPeriods.append({"period": period, "isBooked": isBooked})
        allRooms.append({"room": room, "periods": allPeriods})

    pprint.pprint(allRooms)

    return render(
        request,
        'find.html',
        context={'bookingDate': bookingDate,
                    'allRooms': allRooms,
                    'periods': Period.objects.all(),
                    'displaydate': displaydate}
        ) 