from django.contrib import admin

from . import models as channel_models
from ..post import models as post_models


# Register your models here.

class PostInline(admin.StackedInline):
    model = post_models.Post


@admin.register(channel_models.Channel)
class ChannelAdmin(admin.ModelAdmin):
    inlines = [PostInline]
    pass


@admin.register(channel_models.Topic)
class TopicAdmin(admin.ModelAdmin):
    pass
