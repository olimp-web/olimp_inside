from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext, gettext_lazy as _
from .models import UserAccount, Profile
from api.models import MacModelUser

# Register your models here.


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ('username', 'email', 'profile')


class MACAddressInline(admin.StackedInline):
    model = MacModelUser
    field = ('mac_address', )
    extra = 1


@admin.register(UserAccount)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_full_name')
    search_fields = ('username', 'email', 'patronymic', 'name', 'surname')
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
    inlines = (MACAddressInline, )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patronymic', 'phone_number')
    search_fields = ('patronymic', 'name', 'surname')
