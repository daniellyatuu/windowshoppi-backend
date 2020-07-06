from django.urls import path
from . import views

app_name = 'bussiness_post'

urlpatterns = [
    path('create/', views.CreatePostView.as_view(), name='create_post'),
    path('all/', views.AllPost.as_view(), name='all_post'),
    path('vendor-post/', views.VendorPost.as_view(), name='vendor_post'),
]
