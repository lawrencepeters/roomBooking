from django.shortcuts import render

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

    return render(
        request,
        'find.html',
        context={},
    ) 