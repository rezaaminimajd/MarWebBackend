from django.urls import path
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
    path('profile/<slug:username>', views.ProfileView.as_view()),
    path('profile/id/<int:user_id>',views.ProfileByIdView.as_view()),
    path('follow/<slug:username>', views.FollowUserView.as_view()),
    path('reset_password', views.ResetPasswordView.as_view()),
    path('followers/<slug:username>', views.GetFollowersView.as_view()),
    path('password/reset', views.ForgotPasswordView.as_view()),
    path('password/reset/confirm', views.ForgotPasswordConfirmView.as_view()),

]
