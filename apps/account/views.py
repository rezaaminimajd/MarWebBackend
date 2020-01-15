from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework import status, permissions
from rest_framework.response import Response

from .serializers import *


class SignUpView(GenericAPIView):
    serializer_class = UserSerializers

    def post(self, request):
        serializer: UserSerializers = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': f'{request.data["username"]} created successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': f'{serializer.errors}'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class LogoutView(GenericAPIView):
    pass


class ResetPasswordView(GenericAPIView):
    pass


class ProfileView(GenericAPIView):
    pass


class FollowView(GenericAPIView):
    pass
