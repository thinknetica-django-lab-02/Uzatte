"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.urls import include, path
from django.views.decorators.cache import cache_page

from . import views

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.index, name='index'),
    path('goods/', cache_page(CACHE_TTL)(views.GoodList.as_view()),
         name='goods'),
    path('goods/add/', views.GoodCreate.as_view(), name='good-add'),
    path('goods/<pk>/', views.GoodDetail.as_view(), name='good-detail'),
    path('goods/<pk>/edit', views.GoodEdit.as_view(), name='good-edit'),
    path('accounts/profile/', views.ProfileUpdate.as_view(), name='profile'),
    path('accounts/profile/phone_confirm', views.phone_number_confirmation,
         name='phone-confirm'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
