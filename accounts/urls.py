from django.conf.urls import url, include

from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.index, name='auth'),
    path('reg/', views.reg, name='reg'),
    # url(r'^accounts/', include('django.contrib.auth.urls')),
]