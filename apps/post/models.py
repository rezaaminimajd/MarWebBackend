import os

from django.db import models

from polymorphic.models import PolymorphicModel


# Create your models here.


class UserActionTemplate(PolymorphicModel):
    from ..account.models import Profile
    profile = models.ForeignKey(Profile, related_name='actions', on_delete=models.CASCADE)
    body = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class Post(UserActionTemplate):

    def upload_path(self, filename):
        return os.path.join('private/', self.profile.user.username, 'posts', str(self.id), filename)

    title = models.CharField(max_length=200)
    media = models.FileField(upload_to=upload_path)


class Comment(UserActionTemplate):

    def upload_path(self, filename):
        return os.path.join('private/', self.profile.user.username, 'comments', f'post{self.post.id}', str(self.id),
                            filename)

    media = models.FileField(upload_to=upload_path)
    post_related = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    replies = models.ForeignKey('self', related_name='comments', on_delete=models.CASCADE, null=True, blank=True)


class Like(models.Model):
    from ..account.models import Profile
    target = models.ForeignKey(UserActionTemplate, related_name='likes', on_delete=models.CASCADE)
    liker = models.ForeignKey(Profile, related_name='likes', on_delete=models.CASCADE)
