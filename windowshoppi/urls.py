"""windowshoppi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('app.user.api.urls')),
    # path('business/', include('app.account.api.urls')),  # will be removed
    # path('post1/', include('app.bussiness_post.api.urls')),  # will be removed
    path('account/', include('app.account.api.urls', namespace='account')),
    path('business/', include('app.account.api.urls', namespace='business')),
    path('post/', include('app.account_post.api.urls')),
    path('master_data/', include('app.master_data.api.urls')),
    path('admin/', admin.site.urls),
]

admin.site.site_header = 'windowshoppi adminstration'
admin.site.site_title = 'windowshoppi admin'

if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
