from django import forms
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from mdeditor.fields import MDTextFormField

from .models import Ruleset, Subpage, RecommendBeatmap


class RulesetForm(forms.ModelForm):
    """Form on create and edit the Ruleset object."""
    name = forms.CharField(required=True)
    description = forms.CharField(required=True, widget=forms.Textarea)
    content = MDTextFormField()
    source = forms.URLField(label="Source")

    class Meta:
        model = Ruleset
        fields = ['name', 'description', 'icon', 'light_icon', 'logo', 'cover_image', 'cover_image_light',
                  'opengraph_image', 'recommend_beatmap_cover', 'content', 'source', 'github_download_filename']


class SubpageForm(forms.ModelForm):
    """Form on create and edit the Subpage object."""
    title = forms.CharField(required=True)
    content = MDTextFormField()

    class Meta:
        model = Subpage
        fields = ['title', 'content']


class RecommendBeatmapForm(forms.ModelForm):
    """Form on create RecommendBeatmap object or adding a recommend beatmap."""
    beatmap_id = forms.CharField(required=True)
    comment = forms.CharField(required=True)

    class Meta:
        model = RecommendBeatmap
        fields = ['beatmap_id', 'comment']
