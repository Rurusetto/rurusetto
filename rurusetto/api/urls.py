from django.urls import path
from . import views

urlpatterns = [
    path('rulesets', views.listing),
    path('rulesets/<slug:slug>', views.ruleset_detail),
    path('subpage/<slug:rulesets_slug>', views.all_ruleset_subpage),
    path('subpage/<slug:rulesets_slug>/<slug:subpage_slug>', views.subpage)
]
