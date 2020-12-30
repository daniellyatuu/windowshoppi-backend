from django.urls import path
from . import views

app_name = 'account_post'

urlpatterns = [
    path('create-post/', views.CreatePostView.as_view(), name='create_post'),
    path('post-data/<int:pk>/',
         views.SingleUserAccountPostView.as_view(), name='post_data'),
    path('create/', views.CreatePostViewOld.as_view(),
         name='create_post'),  # will be removed
    path('user-post/<int:pk>/', views.UserAccountPostView.as_view(), name='user_post'),
    path('vendor/', views.UserAccountPostView.as_view(),
         name='vendor_post'),  # will be removed
    path('search-post/', views.SearchPost.as_view(), name='search_post'),
    path('search/', views.SearchPostOld.as_view(),
         name='search_post_old'),  # will be removed
    path('update-post/<int:pk>/', views.UpdatePost.as_view(), name='update_post'),
    path('vendor/<int:pk>/', views.BusinessPost.as_view(),
         name='business_post'),  # will be removed
    path('account/<int:pk>/', views.AccountPostView.as_view(), name='account_post'),
    path('all/', views.AllPost.as_view(), name='all_post'),  # will be removed
    path('post-list/', views.AccountPostListView.as_view(), name='all_account_post'),
    path('search/<int:pk>/', views.AllPost.as_view(),
         name='search_post_by_category'),  # will be removed
]
