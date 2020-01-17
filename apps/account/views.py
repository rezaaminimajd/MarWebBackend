from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework import status, permissions
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .serializers import *


class SignUpView(GenericAPIView):
    serializer_class = UserSerializers

    def post(self, request):
        serializer: UserSerializers = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = True
            user.save()
            print(user.is_active)
            return Response({'detail': f'{request.data["username"]} created successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': f'{serializer.errors}'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class LoginView(GenericAPIView):

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = get_object_or_404(User, username=username)
        ProfileToken.objects.create(profile=user.profile, date=datetime.now())
        if not check_password(password, user.password):
            return Response({'detail': 'password is wrong'}, status=status.HTTP_403_FORBIDDEN)
        user.is_active = True
        user.save()
        return Response({'detail': 'login successfully'}, status=status.HTTP_200_OK)


class LogoutView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user: User = request.user
        user.is_active = False
        user.save()
        return Response({'detail': 'logout successfully'}, status=status.HTTP_200_OK)


class ResetPasswordView(GenericAPIView):
    def post(self, request):
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        repeat_new_password = request.data['repeat_new_password']
        user: User = request.user
        if not check_password(old_password, user.password):
            return Response({'detail': 'password is wrong'}, status=status.HTTP_403_FORBIDDEN)
        if new_password != repeat_new_password:
            return Response({'detail': 'new passwords don\'t match'}, status=status.HTTP_403_FORBIDDEN)
        user.password = make_password(new_password)
        user.save()
        return Response({'detail': 'password change successfully'}, status=status.HTTP_200_OK)


class ProfileView(GenericAPIView):
    serializer_class = ProfileSerializers

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = user.profile
        data = self.get_serializer(profile).data
        return Response(data=data, status=status.HTTP_200_OK)


class FollowUserView(GenericAPIView):
    serializer_class = PolymorphicFollowSerializers

    def post(self, request, username):
        source: User = request.user
        target: User = get_object_or_404(User, username=username)
        FollowUser.objects.create(source=source.profile, target=target.profile, follow_type=FollowTypes.USER)
        return Response(status=status.HTTP_200_OK)
