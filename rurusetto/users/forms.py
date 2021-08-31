from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Config, THEME, SUBPAGE_INDEX


class ProfileUpdateForm(forms.ModelForm):
    """Form in user settings page to update the user's Profile object."""
    about_me = forms.CharField(required=False)
    osu_username = forms.CharField(max_length=20, required=False)

    class Meta:
        model = Profile
        fields = ['about_me', 'cover', 'image', 'osu_username']


class UserUpdateForm(forms.ModelForm):
    """Form in user's settings page to update value in default Django User model."""
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileEveryLoginConfigForm(forms.ModelForm):
    """Form to update update_profile_every_login in user's config model specifically."""
    update_profile_every_login = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': "form-check-input"}))

    class Meta:
        model = Config
        fields = ['update_profile_every_login']


class UserConfigForm(forms.ModelForm):
    """Form to update website theme in user's setting model."""
    theme = forms.ChoiceField(label="", choices=THEME, required=False)

    class Meta:
        model = Config
        fields = ['theme']


class UserSubpageConfigForm(forms.ModelForm):
    """Form to update subpage index design in user's setting model."""
    subpage_index = forms.ChoiceField(label="", choices=SUBPAGE_INDEX, required=False)

    class Meta:
        model = Config
        fields = ['subpage_index']


class UserDeleteAccountForm(forms.ModelForm):
    """Form that show in delete account page. Use to pass the value for verification in delete account views."""
    confirm_username = forms.CharField()
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['confirm_username', 'confirm_password']
