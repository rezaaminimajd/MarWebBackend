from django.contrib import admin
from apps.account.models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = [
        'age',
        'telephone_number',
    ]
    list_display = [
        'id',
        'get_username',
        'get_email',
        'age',
        'telephone_number',
    ]
    list_display_links = ['id']

    def get_username(self, profile: Profile):
        return profile.user.username

    get_username.short_description = 'username'
    get_username.admin_order_field = 'profile_username'

    def get_email(self, profile: Profile):
        return profile.user.email

    get_email.short_description = 'Email'
    get_email.admin_order_field = 'Email'
