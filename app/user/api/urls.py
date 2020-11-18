from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'user'

urlpatterns = [
    path('register/', views.RegisterVendor.as_view(), name='register_user'),
    path('user-data/', views.UserData.as_view(), name='user_data'),
    path('update/', views.UpdateBusinessInfo.as_view(), name='update_account'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('user-login/', views.UserLogin.as_view(), name='user_login'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('validate/', views.ValidateUsername.as_view(), name='validate_username'),
]
