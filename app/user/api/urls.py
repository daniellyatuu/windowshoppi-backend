from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'user'

urlpatterns = [
    path('register/', views.RegisterVendor.as_view(), name='register_user'),
    path('login/', obtain_auth_token, name='login'),
    path('users/', views.UserList.as_view(), name='user_list'),
]
