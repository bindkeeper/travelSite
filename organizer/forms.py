from django import forms
from django.contrib.auth.models import User
from .models import Trip

class TripForm(forms.ModelForm):

	class Meta:
		model = Trip
		
		fields = [
			'startDate',
			'endDate',
			'trip_type',
			'destination',
			'hotel',
			'hotel_price',
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
		
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']