from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import MacModelUser
from accounts.models import UserAccount,Profile
from visits.models import UserInOlimp

# Create your tests here.


class InputTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        _default_profile, _ = Profile.objects.get_or_create(surname="Service", name=":", patronymic=":")
        UserAccount.objects.create(username="test1", email="test1@inside.olimp-union.com", is_active=True, profile=_default_profile)
        MacModelUser.objects.create(user_id=1, mac_address="00:26:57:00:1f:02")
        # print(UserAccount.objects.all().values())
        # print(MacModelUser.objects.all().values())

    def test_create_account(self):
        url = '/api/visits/input_by_mac_addr/'
        data = {
            "mac_address": "00:26:57:00:1f:02"
        }
        print(UserAccount.objects.all().values())
        print(MacModelUser.objects.all().values())

        response = self.client.post(url, data, format='json')
        print("sfsdf")
        print(response.data)
        print()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# class ApiVisitTest(TestCase):
#
    # @classmethod
    # def setUpTestData(cls):
    #     number_entry = 1
#
#     def test_view_url_exist_at_desired_location(self):
#         resp = self.client.get('/api/visits/')
#         self.assertEqual(resp.status_code, 200)

