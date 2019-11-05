from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import MacModelUser
from api.serializers import API_Serializer
from visits.models import Visit
from django.utils import timezone
from django.contrib.auth.decorators import login_required


import re

MAC_PATTERN = "(([0-9A-Fa-f]{2}[-:.]){5}[0-9A-Fa-f]{2})|(([0-9A-Fa-f]{4}\\.){2}[0-9A-Fa-f]{4})"

# Create your views here.
class CustomAPIException(exceptions.APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = 'error'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code
# {"mac_address": "00:26:57:00:1f:02"}



class ApiCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # data = generics.get_object_or_404(MacModelUser.objects.all())
        # serializer = API_Serializer(data)

        # TODO: Возвращать мак адрес конктретного пользователя
        print(MacModelUser.objects.filter(user=request.user).values())
        return Response({"Response": MacModelUser.objects.all().values()})

    def post(self, request):
        data = request.data.get('mac_address')

        if not bool(re.match(MAC_PATTERN, data)):
            raise CustomAPIException({"error": "MAC address not found"}, status_code=status.HTTP_404_NOT_FOUND)

        serializer = API_Serializer(data={"mac_address": data, "user_id": request.user.id})
        if serializer.is_valid(raise_exception=True):
            serializer.save()


        return Response({"Visit": {"mac_address": data}})


        # return Response(mac_validation)
        # check_input =


class ApiInput(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # user = request.user;
        # if request.user.is_authenticated:
        #     user = request.user.username;
        return Response({"User": request.user.username})

    def post(self, request):
        data = request.data.get('mac_address')
        mac_address = MacModelUser.objects.get(mac_address=data, user=request.user)
        if not bool(re.match(MAC_PATTERN, data)) or not mac_address:
            raise CustomAPIException({"error": "MAC address not found"}, status_code=status.HTTP_404_NOT_FOUND)

        try:
            latest_visit = Visit.objects \
                .filter(user=request.user, enter_timestamp__isnull=True) \
                .latest('enter_timestamp')
            latest_visit.enter_timestamp = timezone.now()
            latest_visit.save(update_fields=['enter_timestamp'])
        except Visit.DoesNotExist:
            Visit.objects.create(user=request.user, enter_timestamp=timezone.now())

        return Response({"User in Olimp": request.user.username});


class OutputApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"User": request.user.username})

    def post(self, request):
        data = request.data.get('mac_address')
        mac_address = MacModelUser.objects.get(mac_address=data, user=request.user)
        if not bool(re.match(MAC_PATTERN, data)) or not mac_address:
            raise CustomAPIException({"error": "MAC address not found"}, status_code=status.HTTP_404_NOT_FOUND)

        try:
            latest_visit = Visit.objects\
                .filter(user=request.user, leave_timestamp__isnull=True) \
                .latest('enter_timestamp')
            latest_visit.leave_timestamp = timezone.now()
            latest_visit.save(update_fields=['leave_timestamp'])
        except:
            return Response("User is not defined")

        return Response({"User logged out": request.user.username})


        # data_admin
        # test_1@test.ru
        # username: test_1
        # Pa$$w0rd