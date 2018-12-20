from django.db import models
from accounts.models import AccountManager, UserAccount

# Create your models here.


class Visit(models.Model):
    user = models.ForeignKey('accounts.UserAccount', on_delete=models.CASCADE, related_name='visits')
    enter_timestamp = models.DateTimeField(null=True, blank=True, verbose_name="время входа")
    leave_timestamp = models.DateTimeField(null=True, blank=True, verbose_name="время вЫхода")

    class Meta:
        verbose_name = "посещение"
        verbose_name_plural = "посещения"


class UserInOlimpManager(AccountManager):
    def inside_now(self):
        return self.get_queryset()\
            .annotate(opened_visit=models.Max('visits__enter_timestamp',
                                              filter=models.Q(visits__leave_timestamp__isnull=True)))\
            .filter(opened_visit__isnull=False)
        # return self.get_queryset().filter(id__in=list(users_id))


class UserInOlimp(UserAccount):

    objects = UserInOlimpManager()

    def last_entrance(self):
        _visit = self.visits.latest('enter_timestamp')
        return _visit.enter_timestamp if _visit else None

    @property
    def in_olimp(self):
        return self.visits.latest('enter_timestamp').leave_timestamp is None

    class Meta:
        proxy = True
