from django.urls import path
from .import views

app_name = 'account'

urlpatterns = [
    path('<int:pk>/', views.AccountDetail.as_view(), name='account_detail'),
    path('search-account/', views.SearchAccount.as_view(), name='search_account'),
    path('update-profile-picture/<int:account_id>/', views.UpdateUserProfilePictureView.as_view(),
         name='update_profile_picture'),
    path('remove-profile-picture/<int:account_id>/<int:contact_id>/', views.RemoveProfilePictureView.as_view(),
         name='remove_profile_picture'),
]
