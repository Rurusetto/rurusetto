from django.contrib import admin
from .models import Changelog, Ruleset, CustomWiki, Subpage, RecommendBeatmap, Action

# Register your models here.

admin.site.register(Changelog)
admin.site.register(Ruleset)
admin.site.register(CustomWiki)
admin.site.register(Subpage)
admin.site.register(RecommendBeatmap)
admin.site.register(Action)