from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import MacModelUser
from api.serializers import API_Serializer
from visits.models import Visit
from django.utils import timezone
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)

import re

MAC_PATTERN = "(([0-9A-Fa-f]{2}[-:.]){5}[0-9A-Fa-f]{2})|(([0-9A-Fa-f]{4}\\.){2}[0-9A-Fa-f]{4})"


# {"mac_address": "00:26:57:00:1f:02"}


class ApiCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # TODO: Возвращать мак адрес конктретного пользователя
        return Response({"Response": request.user})

    def post(self, request):
        data = request.data.get('mac_address')

        try:
            if not bool(re.match(MAC_PATTERN, data)):
                raise
        except:
            content = {"error": "Mac address is not correct"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        serializer = API_Serializer(data={"mac_address": data, "user_id": request.user.id})
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response({"Visit": {"mac_address": data}})


class ApiInput(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"User": request.user.username})

    def post(self, request):
        data = request.data.get('mac_address')

        try:
            mac_address = MacModelUser.objects.get(mac_address=data)
            if not bool(re.match(MAC_PATTERN, data)) or not mac_address.user:
                raise
        except:
            content = {'error': "Mac address not found"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            latest_visit = Visit.objects \
                .filter(user=request.user, enter_timestamp__isnull=True) \
                .latest('enter_timestamp')
            latest_visit.enter_timestamp = timezone.now()
            latest_visit.save(update_fields=['enter_timestamp'])
        except Visit.DoesNotExist:
            Visit.objects.create(user=request.user, enter_timestamp=timezone.now())

        return Response({"User in Olimp": request.user.username})


class OutputApi(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"User": request.user.username})

    def post(self, request):
        data = request.data.get('mac_address')

        try:
            mac_address = MacModelUser.objects.get(mac_address=data)
            if not bool(re.match(MAC_PATTERN, data)) or not mac_address.user:
                raise
        except:
            content = {'error': "Mac address not found"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            latest_visit = Visit.objects \
                .filter(user=request.user, leave_timestamp__isnull=True) \
                .latest('enter_timestamp')
            latest_visit.leave_timestamp = timezone.now()
            latest_visit.save(update_fields=['leave_timestamp'])
        except:
            content = {'error': "Mac address not found"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        return Response({"User logged out": request.user.username})

        # data_admin
        # test_1@test.ru
        # username: test_1
        # Pa$$w0rd


# version 1
class CustomPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'results': data
        })


class PaginationApiView(ListAPIView):
    serializer_class = API_Serializer
    pagination_class = CustomPagination
    queryset = MacModelUser.objects.all()


# version 2
class PagApiView(APIView, LimitOffsetPagination):
    default_limit = 10
    max_limit = 1000

    def get(self, request):
        event = MacModelUser.objects.all()
        results = self.paginate_queryset(event, request, view=self)
        serializer = API_Serializer(results, many=True)
        return self.get_paginated_response(serializer.data)


# version 3
class MyPagination(LimitOffsetPagination):
    max_limit = 1000
    default_limit = 1


class PApiView(ListAPIView):
    serializer_class = API_Serializer
    pagination_class = MyPagination
    queryset = MacModelUser.objects.all()
