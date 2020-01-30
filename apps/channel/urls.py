from django.urls import path
from . import views

app_name = 'channel'

urlpatterns = [
    path('channels/', views.ChannelsListAPIView.as_view()),
    path('searchchannels/<slug:search>',views.ChannelsSearchListAPIView.as_view()),
]
