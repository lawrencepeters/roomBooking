from django.shortcuts import render
import datetime
import pprint
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from operator import attrgetter

# Create your views here.

from .models import Room, Facility, RoomFacility, Period, Booking, BookingHistory
@login_required
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

@login_required
def viewbookings(request):
    rooms  = Room.objects.all()
    periods  = Period.objects.all()
    bookingDate = datetime.datetime.now().strftime("%Y-%m-%d")
    if request.method == 'POST':
        bookingDate = datetime.datetime.strptime(request.POST['bookDate'], "%d/%m/%Y").strftime("%Y-%m-%d")

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
                    'displaydate': displaydate}
    ) 

@login_required
def find(request):

    filterRooms = None
    filterPeriods = None    

    bookingDate = datetime.datetime.strptime(request.POST['bookingdate'], "%d/%m/%Y").strftime("%Y-%m-%d")
    requestedRoom = request.POST['roomName']
    requestedPeriod = request.POST['periods']
    requestedFacilities = request.POST.getlist('facilities[]') 

    if requestedRoom == 'any':
        filterRooms = Room.objects.all()
    else:
        filterRooms = Room.objects.filter(roomID = requestedRoom)

    if requestedPeriod == 'any':
        filterPeriods = Period.objects.all()
    else:
        filterPeriods = Period.objects.filter(periodID = requestedPeriod)

    bookedRooms = Booking.objects.filter(date = bookingDate).values('room', 'period')

    displaydate = bookingDate[8:] + "/" + bookingDate[5:-3] + "/" + bookingDate[:4]

    findRooms = []
    for room in filterRooms:
        allPeriods = []
        facilities = []
        facCount = 0
        roomFacilities = RoomFacility.objects.filter(room = room)
        for roomFacility in roomFacilities:
            fac = Facility.objects.filter(facilityID = roomFacility.facility_id)[:1].get()
            if str(roomFacility.facility_id) in requestedFacilities:
                facCount += 1
            facilities.append(fac)
        for period in filterPeriods:
            isBooked = bookedRooms.filter(room = room).filter(period = period).count()

            percentageMatch = 0
            if len(requestedFacilities) > 0:
                percentageMatch = int((facCount/len(requestedFacilities))*100)

            findRooms.append({"bookDate": displaydate,
                                "room": room,
                                "period": period,
                                "isBooked": isBooked,
                                "facilities": facilities,
                                "percentageMatch": percentageMatch
                                })

    sortedRooms = sorted(findRooms, key= lambda x:x['percentageMatch'], reverse=True)

    return render(
        request,
        'find.html',
        context={   'bookingDate': bookingDate,
                    'displaydate': displaydate,
                    'findRooms': sortedRooms
                }
        ) 

@login_required
def mybookings(request):

    bookedRooms = Booking.objects.filter(user = request.user)

    myBookings = []
    for booking in bookedRooms:
        displaydate = booking.date.strftime("%d/%m/%Y")
        myBookings.append({"bookDate": displaydate, "period": booking.period.periodName, "room": booking.room.roomName})

    return render(
        request,
        'mybookings.html',
        context={'myBookings': myBookings}
    )

@login_required
def bookARoom(request):
    pprint.pprint(request.POST)

    bookingDate = request.POST['bookDate']
    period = Period.objects.filter(periodID = request.POST['periodID']).get()
    room = Room.objects.filter(roomID = request.POST['roomID']).get()
    b = Booking(date = bookingDate, room = room, period = period, user = request.user)
    b.save()
    bh = BookingHistory(date = bookingDate, roomName = room.roomName, periodName = period.periodName, username = request.user.username)
    bh.save()
    return HttpResponse()

@login_required
def bookHistory(request):
    bookHistory = BookingHistory.objects.values()

    pprint.pprint(bookHistory)
    
    return render(
        request,
        'bookHistory.html',
        context = {'bookHistory': bookHistory}
    )