from django.db import models

# Create your models here.


class Visit(models.Model):
    user = models.ForeignKey('accounts.UserAccount', on_delete=models.CASCADE, related_name='visits')
    entrance_to_olimp = models.DateTimeField(null=True, blank=True)
    last_visit = models.DateTimeField(null=True, blank=True)