
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from .forms import  UserForm, TripForm
from .models import Trip, Flight, TripType
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View


# Create your views here.

def create_trip(request):
	if not request.user.is_authenticated():
		return render(request, 'organizer/login.html')
	else:
		form = TripForm(request.POST or None)
		if form.is_valid():
			trip = form.save(commit=False)
			trip.user = request.user
			trip.save()
			return render(request, 'organizer/details.html', {'trip' : trip})
		
		trip_types = TripType.objects.all()
		context = {
			"form": form,
			"trip_types" : trip_types
		}
		return render(request, 'organizer/create_trip.html', context)

def delete_trip(request, trip_id):
    trip = Trip.objects.get(pk=trip_id)
    trip.delete()
    all_trips = Trip.objects.filter(user=request.user)
    return render(request, 'organizer/index.html', {'all_trips' : all_trips})		
		

def index(request):
	if not request.user.is_authenticated():
		return render(request, 'organizer/login.html')
	else:
		all_trips = Trip.objects.filter(user=request.user)
	
		return render(request, 'organizer/index.html', {'all_trips' : all_trips})
	'''
	template = loader.get_template('organizer/index.html')
	context = {
		'message': 'Hello2'
	}
	return HttpResponse(template.render(context, request))
	'''
	
	
def detail(request, trip_id):

	'''
	try:
		trip = Trip.objects.get(pk=trip_id)
	except Trip.DoesNotExist:
		raise Http404("Trip Does Not Exist")
	'''
	
	trip = get_object_or_404(Trip, pk=trip_id)
	return render(request, 'organizer/details.html', {'trip' : trip})
	
def favorite(request, trip_id):
	trip = get_object_or_404(Trip, pk=trip_id)
	try:
		selected_trip = trip.flight_set.get(pk=request.POST['trip'])
	except(KeyError, Flight.DoesNotExist):
		return render(request, 'organizer/details.html', {
		'trip' : trip,
		'error_message': "You did not select a valid flight",
		})
	else:
		selected_trip.is_favorite=True
		selected_trip.save()
		return render(request, 'organizer/details.html', {'trip' : trip})

	
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
                return render(request, 'organizer/index.html', {'all_trips': all_trips})
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