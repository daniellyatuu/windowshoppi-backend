from django.urls import path
from . import views

app_name = 'master_data'

urlpatterns = [
    path('', views.CreateCountry.as_view(), name='create_country'),
    path('country/', views.AllCountry.as_view(), name='countries'),
    path('top30category/', views.Top30Category.as_view(), name='top30'),
    path('allCategory/', views.AllCategory.as_view(), name='categories'),
]
