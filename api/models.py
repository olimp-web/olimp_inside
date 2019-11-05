from django.db import models
from accounts.models import UserAccount


# Create your models here.


class MacModelUser(models.Model):
    mac_address = models.CharField(max_length=100, verbose_name="Mac-адресс пользователя")
    user = models.ForeignKey('accounts.UserAccount', on_delete=models.CASCADE, related_name='user_mac_address')

    # user = models.OneToOneField('accounts.UserAccount', on_delete=models.CASCADE)

    def __str__(self):
        return self.mac_address
