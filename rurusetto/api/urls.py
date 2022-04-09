from django.urls import path
from . import views

urlpatterns = [
    path('rulesets', views.listing),
    path('rulesets/<slug:slug>', views.ruleset_detail),
    path('rulesets/<slug:rulesets_slug>/beatmaps', views.recommend_beatmap),
    path('rulesets/<slug:rulesets_slug>/beatmaps/creator', views.recommend_beatmap_only_creator),
    path('rulesets/<slug:rulesets_slug>/beatmaps/players', views.recommend_beatmap_other_players),
    path('subpage/<slug:rulesets_slug>', views.all_ruleset_subpage),
    path('subpage/<slug:rulesets_slug>/<slug:subpage_slug>', views.subpage),
    path('profile/<int:user_id>', views.user),
]
