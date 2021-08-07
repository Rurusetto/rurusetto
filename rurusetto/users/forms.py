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
    class Meta:
        model = Profile
        fields = ['about_me', 'cover', 'image']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField()

    class Meta:
        model = User
        fields = ['username']


class UserConfigForm(forms.ModelForm):

    class Meta:
        model = Config
        fields = ['update_profile_every_login']
