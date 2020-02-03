from django.urls import path

from . import views

app_name = 'post'

urlpatterns = [
    path('posts/hot-posts', views.HotPostsAPIView.as_view(), 'hot_posts'),
    path('posts/new-posts', views.NewPostsAPIVIew.as_view(), 'new_posts'),
    path('posts/followed-channels-post', views.FollowedChannelsPostsAPIView.as_view(), 'followed_channels_post'),
    path('posts/participated-posts', views.ParticipatedPostsAPIView.as_view(), 'participated_posts'),
]
