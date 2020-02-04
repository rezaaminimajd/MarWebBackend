from django.shortcuts import render
from rest_framework import status

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer


# Create your views here.


class UserNotificationsAPIView(GenericAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = self.get_serializer(self.get_queryset().filter(to_user=request.user).filter(seen=False), many=True).data

        return Response(data={'notifications': data}, status=status.HTTP_200_OK)


class MakeNotificationSeenAPIView(GenericAPIView):
    queryset = Notification.objects.all()
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        self.get_queryset().update(seen=True)
        return Response(status=status.HTTP_200_OK)
