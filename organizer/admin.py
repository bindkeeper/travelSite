from django.contrib import admin
from .models import Trip, Flight, TripType, Hotel, Destination, NewTrip, Node, NodeType

admin.site.register(Trip)
admin.site.register(TripType)
admin.site.register(Hotel)
admin.site.register(Destination)
admin.site.register(Flight)
admin.site.register(NewTrip)
admin.site.register(Node)
admin.site.register(NodeType)
