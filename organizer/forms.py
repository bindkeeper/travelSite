from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Trip, NewTrip

class TripForm(forms.ModelForm):

	class Meta:
		model = Trip
		
		fields = [
			'startDate',
			'endDate',
			'trip_type',
			'destination',
			'trip_picture',
			'hotel',
			'hotel_price',
			'existing_hotel',
			'existing_hotel_price',
			'flight_no',
			'flight_price',
			'transport_company', 
			'transport_price',
		]
		
		widgets = {
            'startDate': forms.DateInput(attrs={'class':'date'}),
            'endDate': forms.DateInput(attrs={'class':'date'}),
        }

	def clean(self):
		
		data = super(TripForm, self).clean()
		print(data)
		startDate = data.get('startDate')
		endDate = data.get('endDate')
		if endDate and startDate:
			print('got start and end dates')
			if  not (endDate > startDate):
				print('raising Error')
				raise forms.ValidationError('endDate must be after startDate')
				
		

		return data


		
		
class NewCreateTripForm(forms.ModelForm):
	class Meta:
		model = NewTrip
		
		fields = [
			'startDate',
			'endDate',
			'trip_type',
			'destination',
			'trip_picture',
		]
		
		widgets = {
            'startDate': forms.DateInput(attrs={'class':'date'}),
            'endDate': forms.DateInput(attrs={'class':'date'}),
        }
		
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
		
		
		
class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    



    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')        

    def save(self,commit = True):   
        user = super(MyRegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        

        if commit:
            user.save()

        return user		
		
