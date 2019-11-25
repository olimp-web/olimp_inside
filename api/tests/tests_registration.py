from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase
from api.models import MacModelUser
from accounts.models import UserAccount, Profile
from visits.models import UserInOlimp, Visit
from datetime import datetime


class RegisterationUserTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        _default_profile, _ = Profile.objects.get_or_create(
            surname="Service",
            name=":",
            patronymic=":")
        UserAccount.objects.create(
            username="test1",
            email="test1@inside.olimp-union.com",
            password='secret',
            is_active=True,
            profile=_default_profile
        )
        MacModelUser.objects.create(
            user_id=1,
            mac_address="00:26:57:00:1f:02"
        )

    def test_register_user(self):
        url = '/accounts/register/'
        data = {
            'username': 'test_user',
            'email': 'test@mail.ru',
            'surname': 's_test',
            'name': 'name',
            'patronymic': 'patr',
            'dob': datetime.now(),
            'password1': 'qwerty',
            'password2': 'qwerty',
            'vk_link': 'https://vk.com',
            'phone_number': '89111231234',
        }

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_user_empty_field(self):
        url = '/accounts/register/'
        data = {
            'username': '',
            'email': 'test@mail.ru',
            'surname': '',
            'name': 'name',
            'patronymic': 'patr',
            'dob': datetime.now(),
            'password1': 'qwerty',
            'password2': 'qwerty',
            'vk_link': 'https://vk.com',
            'phone_number': '89111231234',
        }

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
