import secrets

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
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
            return Response({'detail': f'{request.data["username"]} created successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': f'{serializer.errors}'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class LogoutView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user: User = request.user
        user.auth_token.delete()
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

    def put(self, request):
        pass

class ProfileByIdView(GenericAPIView):
    serializer_class = ProfileSerializers

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        profile = user.profile
        data = self.get_serializer(profile).data
        return Response(data=data, status=status.HTTP_200_OK)

    def put(self, request):
        pass


class FollowUserView(GenericAPIView):

    def post(self, request, username):
        source: User = request.user
        target: User = get_object_or_404(User, username=username)
        FollowUser.objects.create(source=source.profile, target=target.profile)
        FollowChannel.objects.create(source=source.profile, target=target.channels.get(main_channel=True))
        return Response(data={"detail": "follow successfully"}, status=status.HTTP_200_OK)


class GetFollowersView(GenericAPIView):
    serializer_class = PolymorphicFollowSerializers

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        followers = user.profile.followers_user.all()
        data = self.get_serializer(followers, many=True).data
        print('data:', data)
        return Response(data={'followers': data}, status=status.HTTP_200_OK)


class GetFollowingView(GenericAPIView):
    serializer_class = PolymorphicFollowSerializers

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        following = user.profile.followings.all()
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
            'domain': 'localhost:8000',
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


class IsFollowingAPIView(GenericAPIView):

    def post(self, request, username):
        user: User = get_object_or_404(User, username=username)
        is_following = False
        if request.user in user.profile.followers_user:
            is_following = True
        return Response(data={'is_following': is_following}, status=status.HTTP_200_OK)
