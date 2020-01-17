from typing import Union, List, Tuple

from ..models import Post
from ...channel.models import Channel


class ChannelPosts:

    def __init__(self, channel_id: int):
        self.channel_id: int = channel_id
        self.posts: Union[List[Post], None] = None
        self.channel: Union[Channel, None] = None
        self.errors: List[str] = []
        self.valid: bool = True

    def __call__(self, *args, **kwargs) -> Tuple[List[Post], List[str]]:
        self._validate_channel()
        if self.valid:
            self._get_posts()
        return self.posts, self.errors

    def _validate_channel(self):
        try:
            self.channel = Channel.objects.get(id=self.channel_id)
        except (Channel.DoesNotExist, Channel.MultipleObjectsReturned) as e:
            self.valid = False
            self.errors.append(str(e))

    def _get_posts(self):
        self.posts = Post.objects.filter(channel=self.channel).order_by('-create_date')
