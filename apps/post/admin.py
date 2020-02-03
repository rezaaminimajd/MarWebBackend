from django.contrib import admin

# Register your models here.


from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from ..post import models as post_models


class CommonAdminFeatures(admin.ModelAdmin):
    readonly_fields = ['type']
    list_display = ['id', '__str__', 'type', 'get_username', 'create_date', 'update_date']
    list_display_links = ['__str__', 'id']
    sortable_by = ['id', 'get_username', 'create_date', 'update_date']
    search_fields = ['get_username']
    list_filter = ['create_date', 'update_date', 'type']

    def get_username(self, user_action: post_models.UserActionTemplate):
        return user_action.user.username

    get_username.short_description = 'User username'
    get_username.admin_order_field = 'user_username'


@admin.register(post_models.UserActionTemplate)
class UserActionAdmin(PolymorphicParentModelAdmin, CommonAdminFeatures):
    base_model = post_models.UserActionTemplate

    child_models = [
        post_models.Post,
        post_models.Comment
    ]

    def has_add_permission(self, request):
        return False


@admin.register(post_models.Post)
class PostAdmin(PolymorphicChildModelAdmin, CommonAdminFeatures):
    base_model = post_models.UserActionTemplate
    show_in_index = True


@admin.register(post_models.Comment)
class CommentAdmin(PolymorphicChildModelAdmin, CommonAdminFeatures):
    base_model = post_models.UserActionTemplate
    show_in_index = True
