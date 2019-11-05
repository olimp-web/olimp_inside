from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext, gettext_lazy as _
from django.shortcuts import render

from .models import UserAccount, Profile


# Register your models here.


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'profile']


@admin.register(UserAccount)
class UserAdmin(UserAdmin):
    list_display = ['username', 'email', 'get_full_name']
    search_fields = ['username', 'email', 'patronymic', 'name', 'surname']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        # (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_form = CustomUserCreationForm
    add_fieldsets = (
        ("TEST", {
            'classes': ('wide',),
            'fields': ('username', 'email', 'profile', 'password1', 'password2'),
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['surname', 'name', 'patronymic', 'phone_number']

    search_fields = ['patronymic', 'name', 'surname']

    def print_doc(self, request, queryset):
        return render(request, 'documents/over_time.html', context={
            "profiles": queryset
        })