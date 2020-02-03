from django.urls import path

from . import views

app_name = 'post'

urlpatterns = [
    path('posts/hot-posts', views.HotPostsAPIView.as_view(), name='hot_posts'),
    path('posts/new-posts', views.NewPostsAPIVIew.as_view(), name='new_posts'),
    path('posts/followed-channels-post', views.FollowedChannelsPostsAPIView.as_view(), name='followed_channels_post'),
    path('posts/participated-posts', views.ParticipatedPostsAPIView.as_view(), name='participated_posts'),
]
