from django.urls import path

from . import views

app_name = 'homepage'

urlpatterns = [
    path('search/<search_query>', views.SearchAPIView.as_view())
]
