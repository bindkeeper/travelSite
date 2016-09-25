from django.conf.urls import url
from . import views

app_name = 'organizer'

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^create_trip/$', views.create_trip, name='create_trip'),
	url(r'^(?P<trip_id>[0-9]+)/delete_trip/$', views.delete_trip, name='delete_trip'),
	
	url(r'^register/$', views.register_with_activation, name='register'),
	url(r'^activate/(?P<key>.+)$', views.activate, name='activate'),
	url(r'^login/$', views.login_user, name='login_user'),
	url(r'^logout_user/$', views.logout_user, name='logout_user'),
	url(r'^trip/(?P<trip_id>[0-9]+)/$', views.details2, name='detail'),
	
	
	url(r'^trip/(?P<trip_id>[0-9]+)/date_change$', views.date_change, name='date_change'),
	url(r'^trip/(?P<trip_id>[0-9]+)/hotel_change$', views.hotel_change, name='hotel_change'),
	url(r'^trip/(?P<trip_id>[0-9]+)/flight_change$', views.flight_change, name='flight_change'),
	url(r'^trip/(?P<trip_id>[0-9]+)/transport_change$', views.transport_change, name='transport_change'),
	url(r'^trip/(?P<trip_id>[0-9]+)/add_flight$', views.add_flight, name='add_flight'),
	
	url(r'^trip/(?P<trip_id>[0-9]+)/add_node$', views.add_node, name='add_node'),
	url(r'^trip/(?P<trip_id>[0-9]+)/node_edit$', views.node_edit, name='node_edit'),
	url(r'^trip/(?P<trip_id>[0-9]+)/node_edit_json$', views.node_edit_json, name='node_edit_json'),
	url(r'^trip/(?P<trip_id>[0-9]+)/node_delete$', views.node_delete, name='node_delete'),
	url(r'^trip/(?P<trip_id>[0-9]+)/share$', views.share, name='share'),
	
	
]