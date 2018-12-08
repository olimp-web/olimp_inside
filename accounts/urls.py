from django.conf.urls import url, include
from django.contrib.auth import views

from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.peopleInside, name='people_in_inside'),
    url(r'open/', views.open, name='open_Olimp'),
    url(r'close/', views.close, name='close_Olimp'),
    url(r'status/', views.status, name='status'),
]