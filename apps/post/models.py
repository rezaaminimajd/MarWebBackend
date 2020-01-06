import os

from django.db import models


# Create your models here.

class Post(models.Model):

    def upload_path(self, filename):
        return os.path.join('private/', self.profile.user.username, 'posts', str(self.id), filename)

    profile = models.ForeignKey('account.Profile', related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    media = models.FileField(upload_to=upload_path)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    def upload_path(self, filename):
        return os.path.join('private/', self.profile.user.username, 'comments', f'post{self.post.id}', str(self.id),
                            filename)

    profile = models.ForeignKey('account.Profile', related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    media = models.FileField(upload_to=upload_path)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
