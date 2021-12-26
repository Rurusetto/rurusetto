from django.urls import path
from . import views

urlpatterns = [
    path('rulesets', views.listing),
    path('rulesets/<slug:slug>', views.ruleset_detail),
]
