from django.urls import path
from . import views

app_name = 'channel'

urlpatterns = [
    path('channels/<username>', views.UserChannelsListAPIView.as_view(), name='user_channels_list'),
    path('channel/create', views.ChannelAPIView.as_view(), name='create_channel'),
    path('top-channels', views.TopChannelsAPIView.as_view(), name='top_channel'),
    path('channel/<int:channel_id>', views.ChannelAPIView.as_view(), name='channel'),
    path('followchannel/<int:channel_id>', views.FollowAPIView.as_view(), name='follow_channel'),
]
