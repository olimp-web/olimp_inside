from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from .views import *

urlpatterns = [
    url(r'add_mac_address/', ApiCreateView.as_view()),

    url(r'input_by_mac_addr/', ApiInput.as_view()),
    url(r'output_by_mac_addr/', OutputApi.as_view()),
]
