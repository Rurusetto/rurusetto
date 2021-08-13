from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Config


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=15, help_text="Required. 15 characters or fewer. Letters, digits and "
                                                        "@/./+/-/_ only.")
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    about_me = forms.CharField(required=False)
    osu_username = forms.CharField(max_length=20, required=False)

    class Meta:
        model = Profile
        fields = ['about_me', 'cover', 'image', 'osu_username']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileEveryLoginConfigForm(forms.ModelForm):
    update_profile_every_login = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': "form-check-input"}))

    class Meta:
        model = Config
        fields = ['update_profile_every_login']


class UserConfigForm(forms.ModelForm):
    theme = forms.CharField

    class Meta:
        model = Config
        fields = ['theme']


class UserDeleteAccountForm(forms.ModelForm):
    confirm_username = forms.CharField()
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['confirm_username', 'confirm_password']
