from django.conf.urls import url, include

from .views import RegistrationFormView

app_name = "register_user"

urlpatterns = [
    url(r'register/', RegistrationFormView.as_view(), name='register'),
]