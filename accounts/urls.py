from django.urls import path, include

from .views import RegistrationFormView

app_name = "accounts"

urlpatterns = [
    path(r'register/', RegistrationFormView.as_view(), name='register'),
    path(r'', include('django.contrib.auth.urls')),
]