from django.contrib import admin

# Register your models here.

from .models import roomInfo
from .models import facilities
from .models import roomFacilities
from .models import periods
from .models import roomAvailability
from .models import bookingRecord
from .models import bookingHistory

admin.site.register(roomInfo)
admin.site.register(facilities)
admin.site.register(roomFacilities)
admin.site.register(periods)
admin.site.register(roomAvailability)
admin.site.register(bookingRecord)
admin.site.register(bookingHistory)