from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import MacModelUser
from api.serializers import API_Serializer, VisitSerializer, VisitDataSerializer
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


class InputByMACView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"User": request.user.username})

    def post(self, request):
        data = request.data.get('mac_address')

        try:
            mac_address = MacModelUser.objects.get(mac_address=data)
            if not bool(re.match(MAC_PATTERN, data)):
                raise
        except:
            content = {'error': "Mac address not found"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            latest_visit = Visit.objects \
                .filter(user=mac_address.user, enter_timestamp__isnull=True) \
                .latest('enter_timestamp')
            if latest_visit.enter_timestamp:
                return Response({"User in Olimp": mac_address.user.username})
            # latest_visit.enter_timestamp = timezone.now()
            # latest_visit.save(update_fields=['enter_timestamp'])
        except Visit.DoesNotExist:
            Visit.objects.create(user=mac_address.user, enter_timestamp=timezone.now())

        return Response({"User in Olimp": mac_address.user.username})


class OutputByMACView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"User": request.user.username})

    def post(self, request):
        data = request.data.get('mac_address')

        try:
            mac_address = MacModelUser.objects.get(mac_address=data)
            if not bool(re.match(MAC_PATTERN, data)):
                raise
        except:
            content = {'error': "Mac address not found"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            latest_visit = Visit.objects \
                .filter(user=mac_address.user, leave_timestamp__isnull=True) \
                .latest('enter_timestamp')
            latest_visit.leave_timestamp = timezone.now()
            latest_visit.save(update_fields=['leave_timestamp'])
        except:
            content = {'error': "Mac address not found"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        return Response({"User logged out": mac_address.user.username})

        # data_admin
        # test_1@test.ru
        # username: test_1
        # Pa$$w0rd


class MyPagination(LimitOffsetPagination):
    max_limit = 1000
    default_limit = 1


class VisitList(ListAPIView):
    serializer_class = VisitDataSerializer
    pagination_class = MyPagination
    queryset = Visit.objects.all()
    #  TODO 1: Add filter by user and Date range
