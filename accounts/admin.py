from django.contrib import admin
from .models import UserAccount, Profile

# Register your models here.


@admin.register(UserAccount)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'get_full_name']
    search_fields = ['username', 'email', 'patronymic', 'name', 'surname']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['surname', 'name', 'patronymic', 'phone_number']

    search_fields = ['patronymic', 'name', 'surname']
