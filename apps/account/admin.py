from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from apps.account.models import *
from apps.post.admin import CommonAdminFeatures


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


@admin.register(Follow)
class FollowAdmin(PolymorphicParentModelAdmin):
    base_model = Follow
    child_models = [FollowUser, FollowChannel]

    def has_add_permission(self, request):
        return False

    readonly_fields = ['follow_type']


@admin.register(FollowUser)
class FollowUserAdmin(PolymorphicChildModelAdmin):
    base_model = Follow
    show_in_index = True

    readonly_fields = ['follow_type']


@admin.register(FollowChannel)
class FollowChannelAdmin(PolymorphicChildModelAdmin):
    base_model = Follow
    show_in_index = True

    readonly_fields = ['follow_type']
