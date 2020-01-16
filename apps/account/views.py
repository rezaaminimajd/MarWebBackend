from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework import status, permissions
from rest_framework.response import Response
import json
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


class LoginView(GenericAPIView):

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = get_object_or_404(User, username=username)
        print(user.username, user.password, password)
        if user.password != password:
            return Response({'detail': 'password is wrong'}, status=status.HTTP_403_FORBIDDEN)
        user.is_active = True
        user.save()
        return Response({'detail': 'login successfully'}, status=status.HTTP_200_OK)


class LogoutView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ResetPasswordView(GenericAPIView):
    pass


class ProfileView(GenericAPIView):
    pass


class FollowView(GenericAPIView):
    pass
