from django.contrib import admin
from .models import UserInOlimp, Visit

# Register your models here.


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('user', 'enter_timestamp', 'leave_timestamp')
    list_filter = ('user', )


@admin.register(UserInOlimp)
class InOlimpAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_full_name', 'in_olimp')

