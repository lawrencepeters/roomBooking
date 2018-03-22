# Import required  modules
from django.shortcuts import render
import datetime
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from operator import attrgetter

# Import relevant models
from .models import Room, Facility, RoomFacility, Period, Booking, BookingHistory

@login_required
# Function to pass through the dropdown values to the index page
def index(request):
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
    bookingDate = datetime.datetime.now().strftime("%Y-%m-%d")   #Creates a datetime object set to today
    if request.method == 'POST':
        bookingDate = datetime.datetime.strptime(request.POST['bookDate'], "%d/%m/%Y").strftime("%Y-%m-%d") # Converts the date posted to a formatted string

    bookedRooms = Booking.objects.filter(date = bookingDate).values('room', 'period')   # Filters Booking objects by date requested 

    displaydate = bookingDate[8:] + "/" + bookingDate[5:-3] + "/" + bookingDate[:4] # Formats bookingDate

    allRooms = []
    for room in Room.objects.all():
        allPeriods = []
        for period in Period.objects.all(): 
            isBooked = bookedRooms.filter(room = room).filter(period = period).count()  # isBooked is a 1 if the room is avaliable, and a 0 if booked
            allPeriods.append({"period": period, "isBooked": isBooked}) # Appends period and isBooked values to allPeriods
        allRooms.append({"room": room, "periods": allPeriods})  # Appends room and allPeriods to allRooms

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

    bookingDate = datetime.datetime.strptime(request.POST['bookingdate'], "%d/%m/%Y")   # Converts the user requested date from a sting to a date
    requestedRoom = request.POST['roomName']    # Gets room
    requestedPeriod = request.POST['periods']   # Gets period
    requestedFacilities = request.POST.getlist('facilities[]')  # Gets list of facilities

    if requestedRoom == 'any':
        filterRooms = Room.objects.all()
    else:
        filterRooms = Room.objects.filter(roomID = requestedRoom)   # Filters rooms by user request

    if requestedPeriod == 'any':   
        filterPeriods = Period.objects.all()
    else:
        filterPeriods = Period.objects.filter(periodID = requestedPeriod)   # Filters periods by user request

    bookedRooms = Booking.objects.filter(date = bookingDate).values('room', 'period')   # Filters rooms by date, room, and period 

    findRooms = []
    for room in filterRooms:
        allPeriods = []
        facilities = []
        facCount = 0
        roomFacilities = RoomFacility.objects.filter(room = room)   # Filters facilities by user request
        for roomFacility in roomFacilities:
            fac = Facility.objects.filter(facilityID = roomFacility.facility_id)[:1].get()  #
            if str(roomFacility.facility_id) in requestedFacilities:                        # Increases the facility count by 1 for each user requested facility 
                facCount += 1                                                               #
            facilities.append(fac)  # Appends the facility object to the facilities list                                                                                           
        for period in filterPeriods:
            isBooked = bookedRooms.filter(room = room).filter(period = period).count()  #isBooked equals 1 if period is free and 0 if booked

            percentageMatch = 0                                                 #
            if len(requestedFacilities) > 0:                                    # Calculate the percentage match of the user requested facilities
                percentageMatch = int((facCount/len(requestedFacilities))*100)  #

            findRooms.append({  "room": room,
                                "period": period,
                                "isBooked": isBooked,
                                "facilities": facilities,
                                "percentageMatch": percentageMatch
                                })

    sortedRooms = sorted(findRooms, key= lambda x:x['percentageMatch'], reverse=True)   # Sort rooms by percentageMatch

    return render(
        request,
        'find.html',
        context={   'bookingDate': bookingDate,
                    'findRooms': sortedRooms
                }
        ) 

@login_required
def mybookings(request):

    myBookings = Booking.objects.filter(user = request.user)    # Filters bookings for user logged in

    return render(
        request,
        'mybookings.html',
        context={'myBookings': myBookings}
    )

@login_required
def bookARoom(request):
    
    bookingDate = datetime.datetime.strptime(request.POST['bookingDate'], "%d/%m/%Y")   # Format date
    period = Period.objects.filter(periodID = request.POST['periodID']).get()   # Filters periods by user requested periods
    room = Room.objects.filter(roomID = request.POST['roomID']).get()   # Filters rooms by user requested rooms
    b = Booking(date = bookingDate, room = room, period = period, user = request.user)  # Creates a booking with the relevant information
    b.save()    # Saves the booking to the database
    bh = BookingHistory(date = bookingDate, roomName = room.roomName, periodName = period.periodName, username = request.user.username) #Creates a history of the booking
    bh.save()   # Saves the booking history to the database
    return HttpResponse()

@login_required
def bookHistory(request):
    bookHistory = BookingHistory.objects.values()   # Gets all values from the booking history

    return render(
        request,
        'bookHistory.html',
        context = {'bookHistory': bookHistory}
    )

@login_required
def roomPopularity(request):

    rp = Booking.objects.values('room_id').annotate(numRooms=Count('room')) # Gets the room_id and the number of times booked 

    roomPopularity = []
    for p in rp:
        r = Room.objects.filter(roomID = p['room_id']).get()    # Filters rooms by id 
        roomPopularity.append({"roomName": r.roomName, "numRooms": p['numRooms']})  # The Name and number of times booked are appended to the roomPopularity array 

    sortedRoomPopularity = sorted(roomPopularity, key= lambda x:x['numRooms'], reverse=True)    # Sort roomPopularity by number of times booked

    return render(
        request,
        'roomPopularity.html',
        context={'roomPopularity': sortedRoomPopularity}
    )

@login_required
def facilityPopularity(request):

    fp = Booking.objects.values()   # Gets all values from booking objects

    fpDict = {}
    for p in fp:
        rf = RoomFacility.objects.filter(room_id = p['room_id']).values()   # Gets all facilities for the room with the corresponding room_id
        for f in rf:
            fac = Facility.objects.filter(facilityID = f['facility_id']).get()  # Gets the facility from the corresponding facility_id
            if fac.facilityName not in fpDict:
                fpDict[fac.facilityName] = 0    # Adds the facility to the dictionary if it does not already exist
            fpDict[fac.facilityName] += 1       # Adds one to the count of the facilty in the dictionary

    facilityPopularity = []
    for f in fpDict:
        facilityPopularity.append({'facilityName': f, 'facCount': fpDict[f]})   # Converts the dictionary to a list object

    sortedFacilityPopularity = sorted(facilityPopularity, key= lambda x:x['facCount'], reverse=True)    # Sort facilityPopularity by number of times booked

    return render(
        request,
        'facilityPopularity.html',
        context={'facilityPopularity': sortedFacilityPopularity}
    )