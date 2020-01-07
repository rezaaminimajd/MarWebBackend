from django.contrib import admin
from apps.account.models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
        'Email',
        'age',
        'telephone_number',
    ]
    list_display = [
        'name',
        'Email',
        'age',
        'telephone_number',
    ]
    list_editable = list_display
    list_display_links = None
