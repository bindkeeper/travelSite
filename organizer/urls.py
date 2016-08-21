from django.conf.urls import url
from . import views

app_name = 'organizer'

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^create_trip/$', views.create_trip, name='create_trip'),
	url(r'^(?P<trip_id>[0-9]+)/delete_trip/$', views.delete_trip, name='delete_trip'),
	
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.login_user, name='login_user'),
	url(r'^logout_user/$', views.logout_user, name='logout_user'),
	url(r'^trip/(?P<trip_id>[0-9]+)/$', views.detail, name='detail'),
	
	url(r'^trip/(?P<trip_id>[0-9]+)/favorite$', views.favorite, name='favorite'),
	
	
]