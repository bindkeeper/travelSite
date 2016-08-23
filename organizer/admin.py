from django.contrib import admin
from .models import Trip, Flight, TripType, Hotel, Destination

admin.site.register(Trip)
admin.site.register(TripType)
admin.site.register(Hotel)
admin.site.register(Destination)
admin.site.register(Flight)
