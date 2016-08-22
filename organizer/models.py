from django.contrib.auth.models import Permission, User
from django.db import models


class TripType(models.Model):
	type_name = models.CharField(max_length=20)
	
	def __str__(self):
		return self.type_name

DEFAULT_TRIP_TYPE = 3
class Trip(models.Model):
	user = models.ForeignKey(User, default=1)
	destination = models.CharField(max_length=200)
	hotel = models.CharField(max_length=200)
	flight_no = models.CharField(max_length=200)
	trip_type = models.ForeignKey(TripType, default=DEFAULT_TRIP_TYPE, on_delete=models.SET_DEFAULT)
	
	'''
	def get_absolute_url(self):
		return reverse('organizer:detail', kwargs={'pk':self.pk})
	
	'''
	def __str__(self):
		return self.destination + " - " + self.hotel
		
		
		

	
	
class Flight(models.Model):
	trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
	ticket_number = models.CharField(max_length=200)
	is_favorite = models.BooleanField(default=False)
	
	def __str__(self):
		return self.ticket_number
	