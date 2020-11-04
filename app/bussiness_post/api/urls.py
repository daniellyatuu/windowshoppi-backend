from django.urls import path
from . import views

app_name = 'bussiness_post'

urlpatterns = [
    path('create/', views.CreatePostView.as_view(), name='create_post'),
    path('all/', views.AllPost.as_view(), name='all_post'),
    path('vendor/', views.VendorPost.as_view(), name='vendor_post'),
    path('vendor/<int:pk>/', views.BusinessPost.as_view(), name='business_post'),
    path('search/', views.SearchPost.as_view(), name='search_post'),
    path('search/<int:pk>/', views.SearchPostByCategory.as_view(),
         name='search_post_by_category'),
    path('update-post/<int:pk>/', views.UpdatePost.as_view(), name='update_post'),
    # path('image-text/', views.InsertTextToImage.as_view(), name='image_text'),
    path('post-list/', views.PostList.as_view(), name='post_list'),
]
