from django.conf.urls import url, include

from .views import RegistrationUserFormView

app_name = "visits"

urlpatterns = [
    url(r'register/', RegistrationUserFormView.as_view(), name='register'),
]