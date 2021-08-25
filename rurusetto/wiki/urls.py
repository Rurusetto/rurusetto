from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rulesets/', views.listing, name='listing'),
    path('new/', views.create_ruleset, name='create_ruleset'),
    path('changelog/', views.changelog, name='changelog'),
    path('rulesets/<slug:slug>', views.wiki_page, name='wiki'),
    path('rulesets/<slug:slug>/edit', views.edit_ruleset_wiki, name='edit_wiki'),
    path('rulesets/<slug:slug>/new/subpage', views.add_subpage, name='add_subpage'),
    path('install', views.install, name='install'),
    # URL path for API
    path('api/rulesets', views.ruleset_list),
    path('api/rulesets/<slug:slug>', views.ruleset_detail)
]