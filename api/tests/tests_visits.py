from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.utils import json

from api.models import MacModelUser
from accounts.models import UserAccount, Profile
from visits.models import UserInOlimp, Visit
from datetime import datetime


# Create your tests here.


class VisitsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        _default_profile, _ = Profile.objects.get_or_create(surname="Service", name=":", patronymic=":")
        UserAccount.objects.create(
            username="test1",
            email="test1@inside.olimp-union.com",
            password='secret',
            is_active=True,
            profile=_default_profile
        )
        MacModelUser.objects.create(user_id=1, mac_address="00:26:57:00:1f:02")
        Visit.objects.create(
            user_id=1,
            enter_timestamp=datetime(2019, 11, 24, 14, 52, 27, 158578)
        )
        Visit.objects.create(
            user_id=1,
            enter_timestamp=datetime(2019, 11, 24, 14, 52, 27, 158578),
            leave_timestamp=datetime(2019, 11, 26, 14, 52, 27, 158578)
        )

    def test_logging_in_olimp(self):
        url = '/api/visits/input_by_mac_addr/'
        data = {
            "mac_address": "00:26:57:00:1f:02"
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logging_in_olimp_error(self):
        url = '/api/visits/input_by_mac_addr/'
        data = {
            "mac_address": "00:26:57:00:1f:05"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_sign_out_in_olimp(self):
        url = '/api/visits/output_by_mac_addr/'
        data = {
            "mac_address": "00:26:57:00:1f:02"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sign_out_in_olimp_error(self):
        url = '/api/visits/output_by_mac_addr/'
        data = {
            "mac_address": "00:26:57:00:1f:06"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_response_data_visits(self):
        url = '/api/visits/'
        response = self.client.get(path=url)
        data = {
            "count": 2,
            "next": 'http://testserver/api/visits/?limit=1&offset=1',
            "previous": None,
            "results": [
                {
                    "profile": {
                        "id": 1,
                        "fullname": "Service : :"
                    },
                    "enter_timestamp": "2019-11-24T14:52:27.158578+03:00",
                    "leave_timestamp": None
                }
            ]
        }
        self.assertEqual(json.loads(response.content), data)

    def test_response_data_visits_limit(self):
        url = '/api/visits/?limit=2'
        response = self.client.get(path=url)
        data = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "profile": {
                        "id": 1,
                        "fullname": "Service : :"
                    },
                    "enter_timestamp": "2019-11-24T14:52:27.158578+03:00",
                    "leave_timestamp": None
                },
                {
                    "profile": {
                        "id": 1,
                        "fullname": "Service : :"
                    },
                    "enter_timestamp": "2019-11-24T14:52:27.158578+03:00",
                    "leave_timestamp": "2019-11-26T14:52:27.158578+03:00"
                }
            ]
        }
        self.assertEqual(json.loads(response.content), data)

    def test_create_macaddress(self):
        url = '/api/mac_addr/create'
        data = {
            "mac_address": "00:26:57:00:1f:02"
        }

        user = UserAccount.objects.get(username='test1')
        self.client = APIClient()
        self.client.force_authenticate(user=user)


        response = self.client.post(
            url,
            data=data,
            # secure={'email': 'test1@inside.olimp-union.com', 'password': 'secret'},
            format='json'
        )
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
