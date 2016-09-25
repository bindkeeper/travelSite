from django.contrib.auth.models import Permission, User
from django.db import models
from django.conf import settings
from django.db.models.fields.files import ImageFieldFile
from PIL import Image, ExifTags
import io

class ActivationKey(models.Model):
	user_id = models.ForeignKey(User, null=True)
	key = models.CharField(max_length = 100)
	

class TripType(models.Model):
	type_name = models.CharField(max_length=20)
	
	def __str__(self):
		return self.type_name
		

class NodeType(models.Model):
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
	departure_date = models.DateTimeField(null=True)
	
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
		return self.destination 
		

		
class NewTrip(models.Model):
	user = models.ForeignKey(User, default=1)
	shared = models.BooleanField(default=False)
	destination = models.CharField(max_length=200)
	startDate = models.DateField(null=True, blank=True)
	endDate = models.DateField(null=True, blank=True)
	trip_picture = models.ImageField(null=True, blank=True)
	trip_type = models.ForeignKey(TripType, default=DEFAULT_TRIP_TYPE, on_delete=models.SET_DEFAULT, blank=True)
	
	def save(self, *args, **kwargs):
		if self.trip_picture:
			super(NewTrip, self).save(*args, **kwargs)
			path = str(self.trip_picture.path)
			image = Image.open(path)
			
			image.thumbnail((300,300), Image.ANTIALIAS)
			image.save(path, "JPEG")
		super(NewTrip, self).save()
			
            
		
	
class Node(models.Model):
	type = models.ForeignKey(NodeType, default=DEFAULT_TRIP_TYPE, on_delete=models.SET_DEFAULT, blank=True)
	startDate = models.DateField(null=True, blank=True)
	endDate = models.DateField(null=True, blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	trip = models.ForeignKey(NewTrip, default=None, on_delete=models.SET_DEFAULT, blank=True, null=True)
	text = models.CharField(max_length=1000)
	lat = models.DecimalField(null = True, max_digits=9, decimal_places=6)
	lng = models.DecimalField(null = True, max_digits=9, decimal_places=6)
	
	# for flight and transfer
	departure_lat = models.DecimalField(null = True, max_digits=9, decimal_places=6)
	departure_lng = models.DecimalField(null = True, max_digits=9, decimal_places=6)
	
	arrival_lat = models.DecimalField(null = True, max_digits=9, decimal_places=6)
	arrival_lng = models.DecimalField(null = True, max_digits=9, decimal_places=6)
	
	sequance_in_trip = models.IntegerField(null=True)

	