
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from .forms import  UserForm, TripForm, NewCreateTripForm, MyRegistrationForm
from .models import Trip, Flight, TripType, Hotel, NewTrip, Node, NodeType, ActivationKey
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic import View
from datetime import datetime
from django.core.urlresolvers import reverse
import decimal
from django.contrib import messages
from django.core import serializers
import json
from django.template.loader import render_to_string
import requests
import hashlib
import random
from django.db.models import Q
from itertools import chain
# Create your views here.

def create_trip(request):
	print("inside create view ")
	if not request.user.is_authenticated():
		return render(request, 'organizer/login.html')
	else:
		form = NewCreateTripForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			trip = form.save(commit=False)
			trip.user = request.user
			trip.save()
			return redirect(reverse('organizer:detail', kwargs={'trip_id' :   trip.pk}), request)
		
		trip_types = TripType.objects.all()
		context = {
			"form": form,
			"trip_types" : trip_types,
			'loged_user': request.user
		}
		return render(request, 'organizer/create_new_trip.html', context)

def delete_trip(request, trip_id):
	if not request.user.is_authenticated():
		return render(request, 'organizer/login.html')
	try:
		trip = NewTrip.objects.get(pk=trip_id, user=request.user)
		if trip is not None:
			trip.delete()
	except (KeyError, NewTrip.DoesNotExist):
		pass
	return redirect('/organizer/', request)


def search(all_shared_trips, query):
	context = {}
	all_shared_trips = all_shared_trips.filter(
		Q(destination__icontains=query) |
		Q(trip_type__type_name__icontains=query)
		)
	context['search_value'] = query
	context['all_shared_trips'] = all_shared_trips
	print(context)
	return context
		

def index(request):
	if not request.user.is_authenticated():
		
		all_shared_trips = NewTrip.objects.filter(shared=True)
		
		if request.method == "GET":
			query = request.GET.get('q')
			if query:
				return render(request, 'organizer/index.html', search(all_shared_trips, query) )
		return render(request, 'organizer/index.html', context )
	else:
		all_shared_trips = NewTrip.objects.filter(shared=True)
		context = {}
		if request.method == "GET":
			
			query = request.GET.get('q')
			if query:
				context = search(all_shared_trips, query)
				print(context)
			
		all_trips = Trip.objects.filter(user=request.user)
		
		new_form_trips = NewTrip.objects.filter(user=request.user)
		loged_user = request.user
		context['all_trips'] = new_form_trips
		context['loged_user'] = loged_user
		if not loged_user.is_active:
			activate_key = ActivationKey.objects.get(user_id=loged_user.id)
			url="http://localhost:8000/organizer/activate/"+activate_key.key
			context['activate'] = url
		return render(request, 'organizer/index.html', context)
			
	
def detail(request, trip_id):	
	if not request.user.is_authenticated():
		all_shared_trips = Trip.objects.filter(shared=True)
	
		return render(request, 'organizer/details.html', {'trip' : trip})
		
	else:
		trip = get_object_or_404(Trip, pk=trip_id)
		hotels = Hotel.objects.all()
		loged_user = request.user
		if trip.user == request.user:
			return render(request, 'organizer/details.html', {'trip' : trip, "can_delete": True ,'loged_user': loged_user, 'hotels': hotels})
		else:
			return render(request, 'organizer/details.html', {'trip' : trip, 'loged_user': loged_user})
	
def new_detail(request, trip_id):	
	if not request.user.is_authenticated():
		trip = get_object_or_404(NewTrip, pk=trip_id)
		nodes = Node.objects.filter(trip=trip.pk)
		return render(request, 'organizer/new_details.html', {'trip' : trip, 'nodes': nodes})
		
	else:
		trip = get_object_or_404(NewTrip, pk=trip_id)
		nodes = Node.objects.filter(trip=trip.pk)
		types = NodeType.objects.all()
		loged_user = request.user
		if trip.user == request.user:
			return render(request, 'organizer/new_details.html', {'trip' : trip, "can_delete": True ,'loged_user': loged_user, 'nodes': nodes, 'types' : types})
		else:
			return render(request, 'organizer/new_details.html', {'trip' : trip, 'loged_user': loged_user, 'nodes': nodes})
			
def details2(request, trip_id):	
	if not request.user.is_authenticated():
		trip = get_object_or_404(NewTrip, pk=trip_id)
		nodes = Node.objects.filter(trip=trip.pk)
		return render(request, 'organizer/details2.html', {'trip' : trip, 'nodes': nodes})
		
	else:
		trip = get_object_or_404(NewTrip, pk=trip_id)
		nodes = Node.objects.filter(trip=trip.pk)
		types = NodeType.objects.all()
		loged_user = request.user
		if trip.user == request.user:
			return render(request, 'organizer/details2.html', {'trip' : trip, "can_delete": True ,'loged_user': loged_user, 'nodes': nodes, 'types' : types})
		else:
			return render(request, 'organizer/details2.html', {'trip' : trip, 'loged_user': loged_user, 'nodes': nodes})
	
	
def share(request, trip_id):
	trip = get_object_or_404(NewTrip, pk=trip_id)
	try:
		if trip.shared:
			trip.shared = False
		else:
			trip.shared = True
			trip.save()
	except (KeyError, NewTrip.DoesNotExist):
		return JsonResponse({'success': False})
	else:
		all_shared_trips = NewTrip.objects.filter(shared=True)
		html = render_to_string('organizer/index_items.html', {'all_shared_trips': all_shared_trips})
		return JsonResponse({'success': True, 'shared': html})
	
def date_change(request, trip_id):
	trip = get_object_or_404(Trip, pk=trip_id)
	
	if trip.shared is not True:
		trip.startDate =  datetime.strptime(request.POST['startDate'], '%m/%d/%Y')
		trip.endDate = datetime.strptime(request.POST['endDate'], '%m/%d/%Y')
		trip.save()
	return render(request, 'organizer/details.html', {'trip' : trip})
	
	
def hotel_change(request, trip_id):
	trip = get_object_or_404(Trip, pk=trip_id)
	if trip.shared is not True:
		trip.hotel = request.POST['hotel']
		trip.hotel_price = request.POST['hotel_price']
		trip.existing_hotel = Hotel.objects.get(id=request.POST['existing_hotel'])
		trip.save()
	
	return redirect(reverse('organizer:detail', kwargs={'trip_id' :   trip_id}), request)

	
def flight_change(request, trip_id):
	trip = get_object_or_404(Trip, pk=trip_id)
	if trip.shared is not True:
		trip.flight_no = request.POST['flight_no']
		trip.flight_price = request.POST['flight_price']
		trip.save()
	return render(request, 'organizer/details.html', {'trip' : trip})

def transport_change(request, trip_id):
	trip = get_object_or_404(Trip, pk=trip_id)
	if trip.shared is not True:
		trip.transport_company = request.POST['transport_company']
		trip.transport_price = request.POST['transport_price']
		trip.save()
	return redirect('organizer/details.html', request)

	

def add_node(request, trip_id):
	if not request.user.is_authenticated():
		trip = get_object_or_404(NewTrip, pk=trip_id)
		nodes = Node.objects.filter(trip=trip.pk)
		return render(request, 'organizer/new_details.html', {'trip' : trip, 'nodes': nodes})
	node = Node()
	node.trip = NewTrip.objects.get(id=trip_id)
	node.type = NodeType.objects.get(id=request.POST['type'])
	node.save()
	return redirect(reverse('organizer:detail', kwargs={'trip_id' :   trip_id}), request)
	
def add_flight(request, trip_id):
	if not request.user.is_authenticated():
		trip = get_object_or_404(NewTrip, pk=trip_id)
		nodes = Node.objects.filter(trip=trip.pk)
		return render(request, 'organizer/new_details.html', {'trip' : trip, 'nodes': nodes})
	node = Node()
	node.trip = NewTrip.objects.get(id=trip_id)
	
	node.save()
	return redirect(reverse('organizer:detail', kwargs={'trip_id' :   trip_id}), request)
	
def node_edit(request, trip_id):
	if not request.user.is_authenticated():
		trip = get_object_or_404(NewTrip, pk=trip_id)
		nodes = Node.objects.filter(trip=trip.pk)
		return render(request, 'organizer/new_details.html', {'trip' : trip, 'nodes': nodes})
	errors = {}
	node_id = request.POST['node_id']
	node = Node.objects.get(id=node_id)
	price = request.POST['price']
	try:
		float(price)
		node.price = price
	except ValueError:
		pass
	
	try:
		node.startDate = datetime.strptime(request.POST['startDate'], '%m/%d/%Y')
		node.endDate = datetime.strptime(request.POST['endDate'], '%m/%d/%Y')
	except ValueError:
		pass
		
	if "lat" in request.POST and "lng" in request.POST:
		try:
			decimal.Decimal(request.POST['lat'])
			node.lat = request.POST['lat']
		except decimal.InvalidOperation:
			pass
		
		try:
			decimal.Decimal(request.POST['lng'])
			node.lng = request.POST['lng']
		except decimal.InvalidOperation:
			pass
		
	if "departure_lat" in request.POST and "departure_lng" in request.POST:
	
		try:
			decimal.Decimal(request.POST['departure_lat'])
			node.departure_lat = request.POST['departure_lat']
		except decimal.InvalidOperation:
			messages.add_message(request, messages.ERROR , 'We did it!')
			pass
	
		try:
			decimal.Decimal(request.POST['departure_lng'])
			node.departure_lng = request.POST['departure_lng']
		except decimal.InvalidOperation:
			pass
		
	
	if "arrival_lat" in request.POST and "arrival_lng" in request.POST:
		
		try:
			decimal.Decimal(request.POST['arrival_lat'])
			node.arrival_lat = request.POST['arrival_lat']
		except decimal.InvalidOperation:
			pass
		
		try:
			decimal.Decimal(request.POST['arrival_lng'])
			node.arrival_lng = request.POST['arrival_lng']
		except decimal.InvalidOperation:
			pass
		
	
	node.text = request.POST['text']
	node.save()
	return redirect(reverse('organizer:detail', kwargs={'trip_id' :   trip_id}), request)
	
def node_edit_json(request, trip_id):
	if not request.user.is_authenticated():
		return JsonResponse({'success': False})
	errors = {}
	node_id = request.POST['node_id']
	node = Node.objects.get(id=node_id)
	price = request.POST['price']
	try:
		float(price)
		node.price = price
	except ValueError:
		pass
	
	try:
		node.startDate = datetime.strptime(request.POST['startDate'], '%m/%d/%Y')
		node.endDate = datetime.strptime(request.POST['endDate'], '%m/%d/%Y')
	except ValueError:
		pass
		
	if "lat" in request.POST and "lng" in request.POST:
		try:
			decimal.Decimal(request.POST['lat'])
			node.lat = request.POST['lat']
		except decimal.InvalidOperation:
			pass
		
		try:
			decimal.Decimal(request.POST['lng'])
			node.lng = request.POST['lng']
		except decimal.InvalidOperation:
			pass
		
	if "departure_lat" in request.POST and "departure_lng" in request.POST:
	
		try:
			decimal.Decimal(request.POST['departure_lat'])
			node.departure_lat = request.POST['departure_lat']
		except decimal.InvalidOperation:
			messages.add_message(request, messages.ERROR , 'We did it!')
			pass
	
		try:
			decimal.Decimal(request.POST['departure_lng'])
			node.departure_lng = request.POST['departure_lng']
		except decimal.InvalidOperation:
			pass
		
	
	if "arrival_lat" in request.POST and "arrival_lng" in request.POST:
		
		try:
			decimal.Decimal(request.POST['arrival_lat'])
			node.arrival_lat = request.POST['arrival_lat']
		except decimal.InvalidOperation:
			pass
		
		try:
			decimal.Decimal(request.POST['arrival_lng'])
			node.arrival_lng = request.POST['arrival_lng']
		except decimal.InvalidOperation:
			pass
		
	
	node.text = request.POST['text']
	node.save()
	
	item_node = Node.objects.filter(id=node_id)
	
	
	
	#item_node.append({'success': True})
	
	raw_data = serializers.serialize('python', item_node)
	actual_data = [d['fields'] for d in raw_data]
	
	
	
	
	
	#print(actual_data)
	#print(item_node.__dict__)
	
	
	
	return JsonResponse({'success': True, 'node': actual_data[0]})
		
	
def node_delete(request, trip_id):
	node_id = request.POST['node_id']
	
	try:
		node = Node.objects.get(pk=node_id)
		if node is not None:
			node.delete()
	except (KeyError, Node.DoesNotExist):
		pass
	return redirect(reverse('organizer:detail', kwargs={'trip_id' :   trip_id}), request)

def send_simple_message(*to_emails):
	return requests.post(
		"https://api.mailgun.net/v3/sandbox0ffbf75a17774b31b46eb945011bc415.mailgun.org/messages",
		auth=("api", "key-3f6cfbf25e83673859ff2a332ab06d10"),
		data={"from": "Excited User <mailgun@sandbox0ffbf75a17774b31b46eb945011bc415.mailgun.org>",
		"to": to_emails,
		"subject": "Hello",
		"text": "Testing some Mailgun awesomness!"})
	
def send_activation(to_email, url):
	return requests.post(
		"https://api.mailgun.net/v3/sandbox0ffbf75a17774b31b46eb945011bc415.mailgun.org/messages",
		auth=("api", "key-3f6cfbf25e83673859ff2a332ab06d10"),
		data={"from": "Excited User <mailgun@sandbox0ffbf75a17774b31b46eb945011bc415.mailgun.org>",
		"to": to_email,
		"subject": "Hello",
		"text": "Please got to this link " + url})
	
def register(request):
	form = MyRegistrationForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password1']
		user.set_password(password)
		user.save()
		url = "http://localhost:8000/organizer/activate/"+user.username
		send_activation(user.email, url)
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				all_trips = Trip.objects.filter(user=request.user)
				return render(request, 'organizer/index.html', {'all_trips': all_trips})
	context = {
		"form": form,
	}
	return render(request, 'organizer/register.html', context)
	
def register_with_activation(request):
	form = MyRegistrationForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password1']
		user.set_password(password)
		user.is_active = False
		user.save()
		activation_model = ActivationKey()
		activation_model.user_id = user
		nonce = ''.join([str(random.randint(0, 9)) for i in range(4)])
		
		nonce=nonce.encode('utf-8')
		useremail = user.email
		if isinstance(useremail, str):
			useremail = useremail.encode("UTF-8")
		activation_model.key = hashlib.sha1(nonce+useremail).hexdigest()
		activation_model.save()
		
		url = "http://localhost:8000/organizer/activate/"+activation_model.key
		#send_activation(user.email, url) # uncomment after adding email service
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				all_trips = Trip.objects.filter(user=request.user)
				return render(request, 'organizer/index.html', {'all_trips': all_trips})
			else: # get rid of this block after email verification will be operational
				login(request, user)
				all_trips = Trip.objects.filter(user=request.user)
				return render(request, 'organizer/index.html', {'all_trips': all_trips, 'activate': url})
	context = {
		"form": form,
	}
	return render(request, 'organizer/register.html', context)

def activate(request, key):
	try:
		activation = ActivationKey.objects.get(key=key)
		if activation:
			user = activation.user_id
			if user:
				if user.is_active == True:
					message = {"error":"User already active"}
					return render(request, 'organizer/activation_error.html', message)
				else:
					user.is_active=True
					user.save()
					return render(request, 'organizer/activation_success.html')
			else:
				return render(request, 'organizer/index.html')
		else:
			return render(request, 'organizer/index.html')
	except ActivationKey.DoesNotExist:
		return render(request, 'organizer/index.html')
	
	
def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				all_trips = Trip.objects.filter(user=request.user)
				return redirect('/organizer/', request)
			else:
				#return render(request, 'organizer/login.html', {'error_message': 'Your account has been disabled'})
				return redirect('/organizer/', request)
		else:
			return render(request, 'organizer/login.html', {'error_message': 'Invalid login'})
	return render(request, 'organizer/login.html')
	
def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'organizer/login.html', context)