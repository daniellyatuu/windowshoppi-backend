from django.urls import path
from .import views

app_name = 'account'

urlpatterns = [
    path('<int:pk>/', views.AccountDetail.as_view(), name='account_detail'),
    path('search-account/', views.SearchAccount.as_view(), name='search_account'),
]
