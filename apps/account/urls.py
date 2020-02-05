from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from . import views

app_name = 'account'

urlpatterns = [
    path('login', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('profile/<username>', views.ProfileView.as_view()),
    path('profile-update', views.ProfileView.as_view(), name='profile_update'),
    path('password-update', views.ChangePassword.as_view(), name='password_update'),
    path('follow/<username>', views.FollowUserView.as_view()),
    path('reset_password', views.ResetPasswordView.as_view()),
    path('followers/<username>', views.FollowersView.as_view()),
    path('followings/<username>', views.FollowingsView.as_view()),
    path('password/reset', views.ForgotPasswordView.as_view()),
    path('password/reset/confirm', views.ForgotPasswordConfirmView.as_view()),
    path('users', views.AllUsersListAPIView.as_view(), name='users_list'),

]
