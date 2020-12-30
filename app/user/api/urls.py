from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'user'

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register_user'),
    path('login/', views.LoginView.as_view(), name='login'),  # will be removed
    path('user-login/', views.LoginUser.as_view(), name='user_login'),
    path('user-data/', views.UserData.as_view(), name='user_data'),
    path('update-whatsapp-number/<int:contact_id>/', views.UpdateWhatsappNumber.as_view(),
         name='update_whatsapp_number'),
    path('update-windowshopper-profile/<int:account_id>/<int:contact_id>/',
         views.UpdateWindowshopperProfile.as_view(), name='update_windowshopper_profile'),
    path('business-account-switch/<int:account_id>/<int:contact_id>/',
         views.SwitchToBusinessAccount.as_view(), name='business_account_switch'),
    path('update-vendor-profile/<int:account_id>/<int:contact_id>/',
         views.UpdateVendorProfile.as_view(), name='update_vendor_profile'),
    path('change-password/', views.ChangePasswordView.as_view(),
         name='change_password'),
    path('update/', views.UpdateBusinessInfo.as_view(), name='update_account'),
    path('validate/', views.ValidateUsername.as_view(), name='validate_username'),
]
