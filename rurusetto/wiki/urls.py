from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('listing/', views.listing, name='listing'),
    path('new/', views.create_ruleset, name='create_ruleset'),
    path('changelog/', views.changelog, name='changelog'),
    path('rulesets/<slug:slug>', views.wiki_page, name='wiki'),
]