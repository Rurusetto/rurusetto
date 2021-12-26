from django.urls import path
from . import views

urlpatterns = [
    path('rulesets/listing/min', views.ruleset_list_minimize),
    path('rulesets/listing/full', views.ruleset_list_full),
    path('rulesets/get/min/<slug:slug>', views.ruleset_detail_minimize),
    path('rulesets/get/full/<slug:slug>', views.ruleset_detail_full),
]
