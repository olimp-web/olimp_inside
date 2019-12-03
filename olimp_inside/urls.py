"""olimp_inside URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings

from api_core.urls import api_router
from . import views
from accounts.views import PrintPage


admin.site.site_header = settings.ADMIN_SITE_HEADER
# test@reh.com
urlpatterns = [
    url(r'^gates/', include('visits.urls', 'visits')),
    path('admin/', admin.site.urls),
    url(r'accounts/', include('accounts.urls', 'accounts')),
    url(r'api/', include('api.urls')),
    # url(r'people-inside/', include('accounts.urls')),
    # url(r'status/', include('accounts.urls'), name="satatus"),
    # url('auth/', include('accounts.urls')),
    path('api/', include('api_core.urls', namespace='API')),
    path(r'print_docs/<int:pk>/', PrintPage.as_view())
]
