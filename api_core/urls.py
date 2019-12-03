from django.urls import re_path, include
from rest_framework.routers import DefaultRouter

from knowledges.api.viewsets import ArticleViewSet

api_router = DefaultRouter()

api_router.register('posts', ArticleViewSet)

app_name = "API Root"
urlpatterns = api_router.urls
urlpatterns += [
    re_path(r'^api-auth/', include('rest_framework.urls'))
]