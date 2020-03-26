from django.contrib import admin
from django.contrib.admin.options import get_content_type_for_model
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext, gettext_lazy as _
from django_object_actions import DjangoObjectActions
from django.utils import timezone
from django.shortcuts import render

from .models import UserAccount, OrgProfile, ServiceDocument, Profile
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
        (None, {'fields': ('username', 'email', 'password', 'profile')}),
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


@admin.register(Profile, OrgProfile)
class OrgProfileAdmin(admin.ModelAdmin):
    list_display = ['surname', 'name', 'patronymic', 'phone_number']

    search_fields = ['patronymic', 'name', 'surname']


@admin.register(ServiceDocument)
class ServiceDocumentAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ('id', 'doc_type', 'date', 'created_at', 'printed_at')
    list_display_links = ('date',)
    list_filter = ('doc_type', )
    readonly_fields = ('printed_at', 'created_at')

    def print_page(self, request, obj):
        obj.printed_at = timezone.now()
        obj.save()
        LogEntry.objects.log_action(user_id=request.user.pk, change_message="Печать документа",
                                    content_type_id=get_content_type_for_model(obj).pk,
                                    object_id=obj.pk,
                                    object_repr=str(obj),
                                    action_flag=1)
        return render(request, template_name=f'documents/{obj.doc_type}.html', context={
            "doc": obj,
            "empty_line_counter": range(3)
        })
    print_page.short_description = "печать документа"
    print_page.label = "Печать"

    change_actions = ('print_page', )
