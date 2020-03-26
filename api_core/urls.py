from django.urls import re_path, include, path
from rest_framework.routers import DefaultRouter

from api.urls import visits_api_urls
from api.views import ApiCreateView
from knowledges.api.viewsets import ArticleViewSet
api_router = DefaultRouter()

api_router.register('posts', ArticleViewSet)

app_name = "API Root"
urlpatterns = api_router.urls
urlpatterns += [
    re_path(r'^api-auth/', include('rest_framework.urls')),
    path('visits/', include((visits_api_urls, 'visits'))),
    path('mac_addr/create', ApiCreateView.as_view()),
]