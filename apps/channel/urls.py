from django.urls import path
from . import views

app_name = 'channel'

urlpatterns = [
    path('channels/', views.ChannelsListAPIView.as_view(), 'channels_list'),
    path('searchchannels/<slug:search>/', views.ChannelsSearchListAPIView.as_view(), 'search_channels'),
    path('followchannel/', views.FollowAPIView.as_view(), name='follow_channel'),
    path('channel/create', views.ChannelAPIView.as_view(), name='create_channel'),
]
