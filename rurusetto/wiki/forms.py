from django import forms
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from mdeditor.fields import MDTextFormField

from .models import Ruleset


class RulesetForm(forms.ModelForm):
    name = forms.CharField(required=True)
    description = forms.CharField(required=True, widget=forms.Textarea)
    content = MDTextFormField()
    github_link = forms.URLField

    class Meta:
        model = Ruleset
        fields = ['name', 'description', 'icon', 'logo', 'cover_image', 'content', 'github_link']
