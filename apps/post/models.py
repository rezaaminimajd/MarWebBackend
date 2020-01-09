import os

from django.db import models

from polymorphic.models import PolymorphicModel


# Create your models here.

class UserActionTypes:
    POST = 'post'
    COMMENT = 'comment'
    TYPES = (
        (POST, 'post'),
        (COMMENT, 'comment')
    )


class UserActionTemplate(PolymorphicModel):
    profile = models.ForeignKey('account.Profile', related_name='actions', on_delete=models.CASCADE)
    body = models.TextField()
    type = models.CharField(max_length=20, choices=UserActionTypes.TYPES)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def upload_path(self, filename):
        return os.path.join('private/', self.profile.user.username, 'actions', str(self.id), filename)

    media = models.FileField(upload_to=upload_path)

    @property
    def post_summary(self):
        return self.body[:len(self.body) // 4]

    def __str__(self):
        return f'id:{self.id}, username:{self.profile.user.username}'


class Post(UserActionTemplate):
    title = models.CharField(max_length=200)

    def pre_save(self):
        self.type = UserActionTypes.POST

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'id:{self.id}, username:{self.profile.user.username}'


class Comment(UserActionTemplate):
    post_related = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    replies = models.ForeignKey('self', related_name='comments', on_delete=models.CASCADE, null=True, blank=True)

    def pre_save(self):
        self.type = UserActionTypes.COMMENT

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'id:{self.id}, username:{self.profile.user.username}'


class Like(models.Model):
    target = models.ForeignKey('post.UserActionTemplate', related_name='likes', on_delete=models.CASCADE)
    liker = models.ForeignKey('account.Profile', related_name='likes', on_delete=models.CASCADE)
