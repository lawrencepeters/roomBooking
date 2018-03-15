from django.shortcuts import render
import datetime
import pprint
from django.contrib.auth.models import User
from django.db.models import Count
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

    #Convert date in request from a sting to a date
    bookingDate = datetime.datetime.strptime(request.POST['bookingdate'], "%d/%m/%Y")
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

            findRooms.append({  "room": room,
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
                    'findRooms': sortedRooms
                }
        ) 

@login_required
def mybookings(request):

    myBookings = Booking.objects.filter(user = request.user)

    return render(
        request,
        'mybookings.html',
        context={'myBookings': myBookings}
    )

@login_required
def bookARoom(request):
    
    bookingDate = datetime.datetime.strptime(request.POST['bookingDate'], "%d/%m/%Y")
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

    return render(
        request,
        'bookHistory.html',
        context = {'bookHistory': bookHistory}
    )

@login_required
def roomPopularity(request):

    rp = Booking.objects.values('room_id').annotate(numRooms=Count('room'))

    roomPopularity = []
    for p in rp:
        r = Room.objects.filter(roomID = p['room_id']).get()
        roomPopularity.append({"roomName": r.roomName, "numRooms": p['numRooms']})

    sortedRoomPopularity = sorted(roomPopularity, key= lambda x:x['numRooms'], reverse=True)

    return render(
        request,
        'roomPopularity.html',
        context={'roomPopularity': sortedRoomPopularity}
    )

@login_required
def facilityPopularity(request):

    fp = Booking.objects.values()

    fpDict = {}
    for p in fp:
        rf = RoomFacility.objects.filter(room_id = p['room_id']).values()
        for f in rf:
            fac = Facility.objects.filter(facilityID = f['facility_id']).get()
            if fac.facilityName not in fpDict:
                fpDict[fac.facilityName] = 0
            fpDict[fac.facilityName] += 1

    facilityPopularity = []
    for f in fpDict:
        facilityPopularity.append({'facilityName': f, 'facCount': fpDict[f]})
    pprint.pprint(facilityPopularity)

    sortedFacilityPopularity = sorted(facilityPopularity, key= lambda x:x['facCount'], reverse=True)

    return render(
        request,
        'facilityPopularity.html',
        context={'facilityPopularity': sortedFacilityPopularity}
    )