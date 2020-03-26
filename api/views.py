from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import MacModelUser
from api.serializers import (
    API_Serializer,
    VisitDataSerializer,
    MACAddressSerializer
)
from visits.models import Visit, UserAccount
from django.utils import timezone
from rest_framework.pagination import LimitOffsetPagination
from django.core.exceptions import ValidationError
import datetime
from rest_framework.filters import SearchFilter
# import logging


# logger = logging.getLogger(__name__ + ".log")
# logging.basicConfig(level=logging.DEBUG, )
# {"mac_address": "00:26:57:00:1f:02"}


class ApiCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # TODO: Возвращать мак адрес конктретного пользователя
        return Response({"Response": request.user.username})

    def post(self, request):
        data = request.data.get('mac_address')

        try:
            serializer = MACAddressSerializer(data={"mac_address": data, "user": request.user.id})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({"Visit": {"mac_address": data}})
        except ValueError:
            content = {"error": "Mac address is not correct"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class InputByMACView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"User": request.user.username})

    def post(self, request):
        data = request.data.get('mac_address')

        try:
            mac_address = MacModelUser.objects.get(mac_address=data)
        except MacModelUser.DoesNotExist:
            content = {'error': "Mac address not found"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            latest_visit = Visit.objects \
                .filter(user=mac_address.user, enter_timestamp__isnull=False,
                        leave_timestamp__isnull=True).latest('enter_timestamp')
            latest_visit.leave_timestamp = timezone.now()
            latest_visit.save(update_fields=['leave_timestamp'])

        except Visit.DoesNotExist:
            pass
        finally:
            Visit.objects.create(user=mac_address.user, enter_timestamp=timezone.now())
        return Response({"User in Olimp": mac_address.user.username})


class OutputByMACView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"User": request.user.username})

    def post(self, request):
        data = request.data.get('mac_address')
        print(data)
        try:
            mac_address = MacModelUser.objects.get(mac_address=data)
        except MacModelUser.DoesNotExist:
            content = {'error': "Mac address not found"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        try:
            latest_visit = Visit.objects \
                .filter(user=mac_address.user, leave_timestamp__isnull=True) \
                .latest('enter_timestamp')
            latest_visit.leave_timestamp = timezone.now()
            latest_visit.save(update_fields=['leave_timestamp'])
            return Response({"User logged out": mac_address.user.username})
        except Visit.DoesNotExist:
            print("breakpoint")
            content = {'error': "Opened visit not found"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        # data_admin
        # test_1@test.ru
        # username: test_1
        # Pa$$w0rd
        # ?user=test_1@olimp.com&date_from=2019-11-15&date_to=2019-11-17


class MyPagination(LimitOffsetPagination):
    max_limit = 1000
    default_limit = 1


class VisitList(ListAPIView):
    serializer_class = VisitDataSerializer
    pagination_class = MyPagination
    queryset = Visit.objects.all()

    def filter_queryset(self, queryset):
        try:
            user = UserAccount.objects.get(id=self.request.query_params.get('user', None))
            queryset = queryset.filter(user=user)
        except (UserAccount.DoesNotExist, TypeError, ValueError):
            pass

        try:
            date_from = datetime.datetime.strptime(
                self.request.query_params.get('date_from', None),
                '%Y-%m-%d')
            queryset = queryset.filter(enter_timestamp__gt=date_from)
        except (TypeError, ValueError):
            pass

        try:
            date_to = datetime.datetime.strptime(
                self.request.query_params.get('date_to', None),
                '%Y-%m-%d')
            queryset = queryset.filter(leave_timestamp__lt=date_to)
        except (TypeError, ValueError):
            pass

        return queryset
