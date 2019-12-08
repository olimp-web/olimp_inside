from django.db import models
from accounts.models import UserAccount


# Create your models here.


class MacModelUser(models.Model):
    PATTERN = r"(([0-9A-Fa-f]{2}[-:._]){5}[0-9A-Fa-f]{2})|(([0-9A-Fa-f]{4}\\.){2}[0-9A-Fa-f]{4})"

    mac_address = models.CharField(max_length=100, verbose_name="Mac-адресс пользователя")
    user = models.ForeignKey('accounts.UserAccount', on_delete=models.CASCADE, verbose_name="Пользователь", related_name='user_mac_address')

    def __str__(self):
        return self.mac_address

    class Meta:
        verbose_name = 'Mac-адрес'
        verbose_name_plural = 'Mac-адреса'
