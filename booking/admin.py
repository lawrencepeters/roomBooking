from django.contrib import admin

# Registration of the models declared in models.py

from .models import Room
from .models import Facility
from .models import RoomFacility
from .models import Period
from .models import Booking
from .models import BookingHistory

admin.site.register(Room)
admin.site.register(Facility)
admin.site.register(RoomFacility)
admin.site.register(Period)
admin.site.register(Booking)
admin.site.register(BookingHistory)