import json
import secrets

import requests
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *


class SignUpView(GenericAPIView):
    serializer_class = UserSerializers

    def post(self, request):
        serializer: UserSerializers = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = True
            user.save()
            return Response({'detail': f'{request.data["username"]} created successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': f'{serializer.errors}'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class LogoutView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user: User = request.user
        user.auth_token.delete()
        return Response({'detail': 'logout successfully'}, status=status.HTTP_200_OK)


class ProfileView(GenericAPIView):
    serializer_class = ProfileSerializers

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = user.profile
        data = self.get_serializer(profile).data
        return Response(data=data, status=status.HTTP_200_OK)

    def put(self, request):
        updated_profile = ProfileUpdateSerializer(instance=request.user, data=request.data)
        if updated_profile.is_valid(raise_exception=True):
            updated_profile.save()
            return Response(data={'detail': 'Profile updated successfully'})
        return Response(data={'errors': 'Profile didn\'t updated'})


class ChangePassword(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
        if not request.user.check_password(data['password']):
            return Response(data={'errors': 'incorrect current password'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        request.user.password = make_password(data['new_password'])
        request.user.save()
        return Response(data={'detail': 'password changed successfully'}, status=status.HTTP_200_OK)


class FollowUserView(GenericAPIView):

    def post(self, request, username):
        source: User = request.user
        target: User = get_object_or_404(User, username=username)
        if FollowUser.objects.filter(source=source, target=target).exists():
            return Response(data={"detail": "Already Followed"}, status=status.HTTP_200_OK)
        FollowUser.objects.create(source=source, target=target)
        FollowChannel.objects.create(source=source, target=target.channels.get(main_channel=True))
        return Response(data={"detail": "follow successfully"}, status=status.HTTP_200_OK)

    def delete(self, request, username):
        target = get_object_or_404(User, username=username)
        deleted, _ = FollowUser.objects.filter(source=request.user, target=target).delete()
        FollowChannel.objects.filter(source=request.user, target=target.channels.get(main_channel=True)).delete()
        if deleted:
            return Response(data={'detail': 'You Successfully unFollowed this user'}, status=status.HTTP_200_OK)
        return Response(data={'errors': 'Unexpected error occurred!'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class FollowersView(GenericAPIView):
    serializer_class = PolymorphicFollowSerializers

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        followers = user.followers_user.all()
        data = self.get_serializer(followers, many=True).data
        print('data:', data)
        return Response(data={'followers': data}, status=status.HTTP_200_OK)


class FollowingsView(GenericAPIView):
    serializer_class = PolymorphicFollowSerializers

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        following = user.followings.all()
        data = self.get_serializer(following, many=True).data
        return Response(data={'followings': data}, status=status.HTTP_200_OK)


class ForgotPasswordView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        data = self.get_serializer(request.data).data
        user = get_object_or_404(User, email=data['email'])

        uid = urlsafe_base64_encode(force_bytes(user.id))
        ForgotPasswordToken.objects.filter(uid=uid).delete()
        reset_password_token = ForgotPasswordToken(
            uid=uid,
            token=secrets.token_urlsafe(32),
            expiration_date=timezone.now() + timezone.timedelta(hours=24),
        )
        reset_password_token.save()

        context = {
            'domain': 'localhost:3000',
            'username': user.username,
            'uid': reset_password_token.uid,
            'token': reset_password_token.token,
        }
        email_html_message = render_to_string('account/email/user_reset_password.html', context)
        email_plaintext_message = render_to_string('account/email/user_reset_password.txt', context)
        msg = EmailMultiAlternatives(
            "Password Reset for {title}".format(title="Marweb Studio"),
            email_plaintext_message,
            "gmail@gmail.com",
            [user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()

        return Response({'detail': 'Successfully Sent Reset Password Email'}, status=200)


class ForgotPasswordConfirmView(GenericAPIView):
    serializer_class = ForgotPasswordConfirmSerializer

    def post(self, request):
        data = self.get_serializer(request.data).data

        rs_token = get_object_or_404(ForgotPasswordToken, uid=data['uid'], token=data['token'])
        if (timezone.now() - rs_token.expiration_date).total_seconds() > 24 * 60 * 60:
            return Response({'error': 'Token Expired'}, status=400)

        user = get_object_or_404(User, id=urlsafe_base64_decode(data['uid']).decode('utf-8'))
        user.password = make_password(data['new_password1'])
        user.save()
        return Response({'detail': 'Successfully Changed Password'}, status=200)


class AllUsersListAPIView(GenericAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()

    def get(self, request):
        data = self.get_serializer(self.get_queryset(), many=True).data
        return Response(data={'users': data}, status=status.HTTP_200_OK)


class GoogleAPIView(GenericAPIView):
    def post(self, request):
        payload = {'access_token': request.data.get("token")}
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(data=content, status=status.HTTP_200_OK)

        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = User()
            user.username = data['email']
            user.password = make_password(BaseUserManager().make_random_password())
            user.email = data['email']
            user.save()
            Profile.objects.create(user=user, age=0, telephone_number='', image=data['picture'])
            channel = Channel.objects.create(creator=user, title=user.username, main_channel=True)
            channel.authors.add(user)

        token = RefreshToken.for_user(user)
        response = {'access_token': str(token.access_token), 'refresh_token': str(token)}
        return Response(data=response, status=status.HTTP_200_OK)
