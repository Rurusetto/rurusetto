from django.contrib import admin
from .models import Profile, Config, Tag

# Register your models here.

admin.site.register(Profile)
admin.site.register(Config)
admin.site.register(Tag)