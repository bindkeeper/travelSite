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
	trip_picture = models.FileField(null=True)
	
	startDate = models.DateField()
	endDate = models.DateField()
	
	hotel = models.CharField(max_length=200)
	hotel_price = models.DecimalField(max_digits=10, decimal_places=2)
	
	existing_hotel = models.ForeignKey(Hotel, default=None, null=True, on_delete=models.SET_DEFAULT)
	existing_hotel_price = models.DecimalField(max_digits=10, decimal_places=2)
	
	flight_no = models.CharField(max_length=200)
	flight_price = models.DecimalField(max_digits=10, decimal_places=2)
	
	transport_company = models.CharField(max_length=200)
	transport_price = models.DecimalField(max_digits=10, decimal_places=2)
	
	trip_type = models.ForeignKey(TripType, default=DEFAULT_TRIP_TYPE, on_delete=models.SET_DEFAULT)
	
	def __str__(self):
		return self.destination + " - " + self.hotel
		
		
		

	
	

	