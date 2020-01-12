from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import status, permissions
from rest_framework.response import Response

from .serializers import *


class SignUpView(GenericAPIView):
    serializer_class = UserSerializers

    def post(self, request):
        serializer = self.get_serializer(request.data)
        serializer.is_valid()
        serializer.save()
        return Response({'detail': 'User created successfully.'}, status=200)


class LogoutView(GenericAPIView):
    pass


class ResetPasswordView(GenericAPIView):
    pass


class ProfileView(GenericAPIView):
    pass


class FollowView(GenericAPIView):
    pass
