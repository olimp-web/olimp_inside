from django.urls import path
from django.conf.urls import include
from .views import *


visits_api_urls = (
    path(r'', VisitList.as_view()),
    path(r'input_by_mac_addr/', InputByMACView.as_view()),
    path(r'output_by_mac_addr/', OutputByMACView.as_view()),
)


# urlpatterns = [
#     path(r'mac_addr/create', ApiCreateView.as_view()),
#     path(r'visits/', include((visits_api_urls, 'visits'), namespace="API/visits")),
# ]
