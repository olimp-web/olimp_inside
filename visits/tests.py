from django.test import TestCase
from django.utils.timezone import now, timedelta

from accounts.models import Profile
from .models import UserInOlimp, Visit


# Create your tests here.


class TestVisits(TestCase):

    def test_who_inside(self):
        _default_profile, _ = Profile.objects.get_or_create(surname="Service", name=":", patronymic=":")
        u1 = UserInOlimp.objects.create(
            username="test1", email="test1@inside.olimp-union.com", is_active=True, profile=_default_profile
        )
        u2 = UserInOlimp.objects.create(
            username="test22", email="test22@inside.olimp-union.com", is_active=True, profile=_default_profile
        )
        u3 = UserInOlimp.objects.create(
            username="test333", email="test333@inside.olimp-union.com", is_active=True, profile=_default_profile
        )
        Visit.objects.create(
            user=u1, enter_timestamp=now() - timedelta(hours=2), leave_timestamp=None
        )
        Visit.objects.create(
            user=u1, enter_timestamp=now() - timedelta(hours=5), leave_timestamp=now() - timedelta(hours=3)
        )
        Visit.objects.create(
            user=u2, enter_timestamp=now() - timedelta(hours=6), leave_timestamp=now() - timedelta(hours=2),
        )

        in_olimp = UserInOlimp.objects.inside_now()
        # for u in in_olimp:
        #     print(u.username, u.opened_visit)
        self.assertEqual(len(in_olimp), 1)
        self.assertEqual(in_olimp[0], u1)
