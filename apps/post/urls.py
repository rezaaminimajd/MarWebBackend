from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('posts/hot-posts', views.HotPostsAPIView.as_view(), name='hot_posts'),
    path('posts/new-posts', views.NewPostsAPIVIew.as_view(), name='new_posts'),
    path('posts/followed-channels-post', views.FollowedChannelsPostsAPIView.as_view(), name='followed_channels_post'),
    path('posts/participated-posts', views.ParticipatedPostsAPIView.as_view(), name='participated_posts'),
    path('post-view', views.PostAPIView.as_view(), name='post'),
    path('post-view/<int:post_id>', views.PostAPIView.as_view(), name=''),
    path('post-view/create', views.PostAPIView.as_view(), name='post_create'),
    path('post-view/detail', views.PostAPIView.as_view(), name='post_details'),
    path('post-view/edit/<int:post_id>', views.PostAPIView.as_view(), name='post_edit'),
    path('post-view/delete/<int:post_id>', views.PostAPIView.as_view(), name='post_delete'),
    path('userposts/<slug:username>', views.UserPostsListAPIView.as_view(), name='user_posts'),
    path('channelposts/<int:channel_id>', views.ChannelPostsListAPIView.as_view(), name='channel_posts'),
    path('like/<int:action_id>', views.LikeAPIView.as_view(), name='like_action'),
    path('dislike/<int:action_id>', views.DisLikeAPIView.as_view(), name='dislike_action'),
    path('insert-comment', views.CommentAPIView.as_view(), name='insert_comment'),
    path('insert-comment/<int:comment_id>', views.CommentAPIView.as_view(), name='update_comment'),
    path('delete-comment/<int:comment_id>', views.CommentAPIView.as_view(), name='delete_comment')

]
