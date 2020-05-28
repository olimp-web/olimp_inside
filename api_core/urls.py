from django.urls import re_path, include, path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token


from api.urls import visits_api_urls
from api.views import ApiCreateView, AuthentificationTokenView, UserRetrieveUpdateAPIView
from knowledges.api.viewsets import ArticleViewSet


api_router = DefaultRouter()

api_router.register('posts', ArticleViewSet)

app_name = "API Root"
urlpatterns = api_router.urls
urlpatterns += [
    re_path(r'^api-auth/', include('rest_framework.urls')),
    path('visits/', include((visits_api_urls, 'visits'))),
    path('mac_addr/create', ApiCreateView.as_view()),

    # Auth with handler generation
    path(r'authorisation/', AuthentificationTokenView.as_view()),
    path('update/', UserRetrieveUpdateAPIView.as_view()),

    # Auth with rest_framework_jwt
    re_path(r'api-token-auth/', obtain_jwt_token),
    re_path(r'^api-token-refresh/', refresh_jwt_token),
    re_path(r'^api-token-verify/', verify_jwt_token),
]