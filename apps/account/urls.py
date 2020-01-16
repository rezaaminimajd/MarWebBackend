from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views

app_name = 'account'

urlpatterns = [
    path('token', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('login', views.LoginView.as_view(), name='login'),
    path('profile/<slug:username>', views.ProfileView.as_view()),

]
