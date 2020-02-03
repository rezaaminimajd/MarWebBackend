from typing import Union, List

from apps.account.models import FollowChannel
from apps.channel.models import Channel


class FollowedChannelsPosts:

    def __init__(self, request):
        self.request = request
        self.followed_channels: Union[List[Channel], None] = None
        self.posts = []
        pass

    def __call__(self):
        self._set_followed_channels()
        self._set_posts()
        return self.posts

    def _set_followed_channels(self):
        self.followed_channels = FollowChannel.objects.filter(
            source=self.request.user).values_list('target', flat=True)

    def _set_posts(self):
        for channel in self.followed_channels:
            self.posts.extend(list(channel.posts.all()))
