#Import default django  modules
from django.conf.urls import url
from . import views

#Declares web pages and links them to the relevant code in views.py

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('viewbookings', views.viewbookings, name='viewbookings'),
    url('find', views.find, name='find'),
    url('mybookings', views.mybookings, name='mybookings'),
    url('bookARoom', views.bookARoom, name='bookARoom'),
    url('bookhistory', views.bookHistory, name='bookHistory'),
    url('roomPopularity', views.roomPopularity, name='roomPopularity'),
    url('facilityPopularity', views.facilityPopularity, name='facilityPopularity')
]

