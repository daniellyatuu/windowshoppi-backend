from django.urls import path
from . import views

app_name = 'master_data'

urlpatterns = [
    path('', views.AllCountry.as_view(), name='countries'),
]
