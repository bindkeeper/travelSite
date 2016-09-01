
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from .forms import  UserForm, TripForm
from .models import Trip, Flight, TripType, Hotel
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from datetime import datetime
from django.core.urlresolvers import reverse

# Create your views here.

def create_trip(request):
	if not request.user.is_authenticated():
		return render(request, 'organizer/login.html')
	else:
		form = TripForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			trip = form.save(commit=False)
			trip.user = request.user
			
			trip.save()
			return render(request, 'organizer/details.html', {'trip' : trip})
		
		trip_types = TripType.objects.all()
		context = {
			"form": form,
			"trip_types" : trip_types,
			'loged_user': request.user
		}
		return render(request, 'organizer/create_trip.html', context)

def delete_trip(request, trip_id):
	if not request.user.is_authenticated():
		return render(request, 'organizer/login.html')
	try:
		trip = Trip.objects.get(pk=trip_id, user=request.user)
		if trip is not None:
			trip.delete()
	except (KeyError, Trip.DoesNotExist):
		pass
	return redirect('/organizer/', request)

		
		

def index(request):
	if not request.user.is_authenticated():
		all_shared_trips = Trip.objects.filter(shared=True)
	
		return render(request, 'organizer/index.html', {'all_shared_trips': all_shared_trips})
	else:
		all_trips = Trip.objects.filter(user=request.user)
		all_shared_trips = Trip.objects.filter(shared=True)
		loged_user = request.user
		return render(request, 'organizer/index.html', {'all_trips' : all_trips, 'all_shared_trips': all_shared_trips, 'loged_user': loged_user})
	
	
	
def detail(request, trip_id):	
	if not request.user.is_authenticated():
		all_shared_trips = Trip.objects.filter(shared=True)
	
		return render(request, 'organizer/index.html', {'all_shared_trips': all_shared_trips})
		
	else:
		trip = get_object_or_404(Trip, pk=trip_id)
		hotels = Hotel.objects.all()
		loged_user = request.user
		if trip.user == request.user:
			return render(request, 'organizer/details.html', {'trip' : trip, "can_delete": True ,'loged_user': loged_user, 'hotels': hotels})
		else:
			return render(request, 'organizer/details.html', {'trip' : trip, 'loged_user': loged_user})
	
def share(request, trip_id):
	trip = get_object_or_404(Trip, pk=trip_id)
	try:
		if trip.shared:
			trip.shared = False
		else:
			trip.shared = True
			trip.save()
	except (KeyError, Trip.DoesNotExist):
		return JsonResponse({'success': False})
	else:
		return JsonResponse({'success': True})
	
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

	
def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
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
                return render(request, 'organizer/login.html', {'error_message': 'Your account has been disabled'})
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