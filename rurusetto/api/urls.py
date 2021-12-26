from django.urls import path
from . import views

urlpatterns = [
    path('api/rulesets', views.ruleset_list),
    path('api/rulesets/<slug:slug>', views.ruleset_detail),
]
