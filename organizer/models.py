from django.contrib.auth.models import Permission, User
from django.db import models


class TripType(models.Model):
	type_name = models.CharField(max_length=20)
	
	def __str__(self):
		return self.type_name
		
		
		
class Hotel(models.Model):
	hotel_name = models.CharField(max_length=20)
	def __str__(self):
		return self.hotel_name
	
class Destination(models.Model):
	destination = models.CharField(max_length=20)
	destiantion_picture = models.FileField(default=None)
	
	def __str__(self):
		return self.destination
		
		
class Flight(models.Model):
	
	ticket_number = models.CharField(max_length=200)
	is_favorite = models.BooleanField(default=False)
	
	def __str__(self):
		return self.ticket_number

DEFAULT_TRIP_TYPE = 3
class Trip(models.Model):
	shared = models.BooleanField(default=False)
	user = models.ForeignKey(User, default=1)
	destination = models.CharField(max_length=200)
	trip_picture = models.FileField(null=True, blank=True)
	
	startDate = models.DateField(null=True, blank=True)
	endDate = models.DateField(null=True, blank=True)
	
	hotel = models.CharField(max_length=200, null=True, blank=True)
	hotel_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	
	existing_hotel = models.ForeignKey(Hotel, default=None, null=True, on_delete=models.SET_DEFAULT, blank=True)
	existing_hotel_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	
	flight_no = models.CharField(max_length=200, null=True, blank=True)
	flight_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	
	transport_company = models.CharField(max_length=200, null=True, blank=True)
	transport_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	
	trip_type = models.ForeignKey(TripType, default=DEFAULT_TRIP_TYPE, on_delete=models.SET_DEFAULT, blank=True)
	
	def __str__(self):
		return self.destination + " - " + self.hotel
		
		
		

	
	

	