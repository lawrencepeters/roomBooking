from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('viewbookings', views.viewbookings, name='viewbookings'),
    url('find', views.find, name='find'),
    url('mybookings', views.mybookings, name='mybookings')
]

