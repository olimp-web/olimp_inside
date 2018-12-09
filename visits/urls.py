from django.conf.urls import url, include

from .views import people_inside, open, close, status

app_name = "visits"

urlpatterns = [
    url(r'^$', people_inside, name='people_inside'),
    url(r'^open/$', open, name='open'),
    url(r'^close/$', close, name='close'),
    url(r'^status/$', status, name='status'),
]