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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpResponse
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from . import api
from . import views
from .sitemaps import GoodSitemap
from rest_framework.authtoken import views as authviews

router = DefaultRouter()
router.register('goods', api.GoodViewSet)

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

sitemaps = {
    'goods': GoodSitemap,
}

robots = """
User-Agent: *\nDisallow: /admin\nSitemap /sitemap.xml
"""

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('contacts/', views.contacts),
    path('delivery/', views.delivery),
    path('about/', views.about),
    path('goods/', views.GoodList.as_view(),
         name='goods'),
    path('goods/add/', views.GoodCreate.as_view(), name='good-add'),
    path('goods/<pk>/', views.GoodDetail.as_view(), name='good-detail'),
    path('goods/<pk>/edit', views.GoodEdit.as_view(), name='good-edit'),
    path('accounts/profile/', views.ProfileUpdate.as_view(), name='profile'),
    path('accounts/profile/phone_confirm', views.phone_number_confirmation,
         name='phone-confirm'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    url(r'^robots.txt', lambda x: HttpResponse(robots, content_type="text/plain"),
        name="robots_file"),
    path('api/', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('api-token-auth/', authviews.obtain_auth_token)
]
