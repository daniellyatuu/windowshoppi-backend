from django.urls import path
from . import views

app_name = 'bussiness'

urlpatterns = [
    path('<int:pk>/', views.BusinessInfo.as_view(), name='business_info'),
]
