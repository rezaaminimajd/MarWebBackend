from django.urls import path

from . import views

app_name = 'notification'

urlpatterns = [
    path('notifications', views.UserNotificationsAPIView.as_view(), name='user_notifications'),
    path('seen-notifications', views.UserNotificationsAPIView.as_view(), name='seen_notifications')
]
