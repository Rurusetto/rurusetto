from django.contrib import admin
from .models import Changelog, Ruleset, CustomWiki

# Register your models here.

admin.site.register(Changelog)
admin.site.register(Ruleset)
admin.site.register(CustomWiki)