from django import forms
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from mdeditor.fields import MDTextFormField

from .models import Ruleset, Subpage, RecommendBeatmap


class RulesetForm(forms.ModelForm):
    name = forms.CharField(required=True)
    description = forms.CharField(required=True, widget=forms.Textarea)
    content = MDTextFormField()
    source = forms.URLField(label="Source")

    class Meta:
        model = Ruleset
        fields = ['name', 'description', 'icon', 'logo', 'cover_image', 'opengraph_image', 'content', 'source']


class SubpageForm(forms.ModelForm):
    title = forms.CharField(required=True)
    content = MDTextFormField()

    class Meta:
        model = Subpage
        fields = ['title', 'content']


class RecommendBeatmapForm(forms.ModelForm):
    beatmap_id = forms.CharField(required=True)
    comment = forms.CharField(required=True)

    class Meta:
        model = RecommendBeatmap
        fields = ['beatmap_id', 'comment']
