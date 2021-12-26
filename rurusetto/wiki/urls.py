from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rulesets/', views.listing, name='listing'),
    path('archived/', views.archived_rulesets, name='archived_rulesets'),
    path('new/', views.create_ruleset, name='create_ruleset'),
    path('changelog/', views.changelog, name='changelog'),
    path('rulesets/<slug:slug>', views.wiki_page, name='wiki'),
    path('rulesets/<slug:slug>/beatmaps', views.recommend_beatmap, name='recommend_beatmap'),
    path('rulesets/<slug:slug>/edit', views.edit_ruleset_wiki, name='edit_wiki'),
    path('rulesets/<slug:slug>/new/subpage', views.add_subpage, name='add_subpage'),
    path('rulesets/<slug:rulesets_slug>/<slug:subpage_slug>', views.subpage, name='subpage'),
    path('rulesets/<slug:rulesets_slug>/<slug:subpage_slug>/edit', views.edit_subpage, name='edit_subpage'),
    path('rulesets/<slug:rulesets_slug>/<slug:subpage_slug>/delete', views.delete_subpage, name='delete_subpage'),
    path('rulesets/<slug:slug>/new/beatmaps', views.add_recommend_beatmap, name='add_recommend_beatmap'),
    path('rulesets/<slug:rulesets_slug>/manage/beatmaps', views.recommend_beatmap_approval, name='recommend_beatmap_approval'),
    path('rulesets/<slug:rulesets_slug>/manage/beatmaps/approve/<int:beatmap_id>', views.approve_recommend_beatmap, name='approve_recommend_beatmap'),
    path('rulesets/<slug:rulesets_slug>/manage/beatmaps/deny/<int:beatmap_id>', views.deny_recommend_beatmap, name='deny_recommend_beatmap'),
    path('install', views.install, name='install'),
    path('status', views.status, name='status'),
    path('maintainer', views.maintainer_menu, name='maintainer'),
    path('action/maintainer/update-beatmap', views.update_beatmap_action, name='update_beatmap_action'),
    path('action/maintainer/update-ruleset-version', views.update_ruleset_status_action, name='update_ruleset_version'),
    path('action/maintainer/update-ruleset-version-once', views.update_ruleset_status_once_action, name='update_ruleset_version_once_action'),
    path('action/update/action_log/<int:log_id>', views.check_action_log, name='check_action_log'),
    # URL path for API
    path('api/rulesets', views.ruleset_list),
    path('api/rulesets/<slug:slug>', views.ruleset_detail),
    # Fallback URL path for redirect user who use old website link to the new website path
    path('pages/<slug:slug>', views.redirect_from_old_link, name='redirect_from_old_link')
    path('posts/<slug:slug>', views.redirect_from_old_link, name='redirect_from_old_link_posts')
]
