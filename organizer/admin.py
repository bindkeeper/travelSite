from django.contrib import admin
from .models import Trip, Flight, TripType

admin.site.register(Trip)
admin.site.register(TripType)
admin.site.register(Flight)
