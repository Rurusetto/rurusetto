"""rurusetto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth.models import User
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import resolve_url
from django.urls import path, include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from wiki.models import Ruleset


class WikiSitemap(Sitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return Ruleset.objects.all()

    def location(self, obj):
        return resolve_url('wiki', slug=obj.slug)

    def lastmod(self, obj):
        return obj.last_edited_at


class ProfileSitemap(Sitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return User.objects.all()

    def location(self, obj):
        return resolve_url('profile', pk=obj.id)

    def lastmod(self, obj):
        return obj.date_joined


class StaticSitemap(Sitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return ['listing', 'home', 'changelog']

    def location(self, obj):
        return resolve_url(obj)


sitemaps = {
    'wiki': WikiSitemap,
    'profile': ProfileSitemap,
    'static': StaticSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('wiki.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('mdeditor/', include('mdeditor.urls')),
    path('accounts/', include('allauth.urls')),
    path('register/', user_views.register, name='register'),
    path('profile/<int:pk>', user_views.profile_detail, name='profile'),
    path('settings/', user_views.settings, name='settings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
