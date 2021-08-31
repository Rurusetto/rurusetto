import os
import requests
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile, Config
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.dispatch.dispatcher import receiver
from allauth.account.signals import user_logged_in
from allauth.socialaccount.models import SocialAccount


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """When receive that has user signed up, it will create Profile and Config object that is bind with User object."""
    if created:
        Profile.objects.create(user=instance)
        Config.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Signal when user change something in profile, it will save."""
    instance.profile.save()


@receiver(user_logged_in)
def user_update_information_in_allauth(request, user, **kwargs):
    """Signal when user login using allauth (login with osu! account)"""
    profile = Profile.objects.get(user=request.user)
    # If user login by using osu! account and user login first time or user's config `Update Profile Every Login`
    # is True, start fetch data from extra_data that just get from login system and assign to user's profile
    if (SocialAccount.objects.filter(user=request.user).exists() and not request.user.profile.oauth_first_migrate) or request.user.config.update_profile_every_login:
        data = SocialAccount.objects.get(user=request.user).extra_data

        # If extra data from user detail from osu! API is not None (null in JSON) and it's not default image, can delete
        if request.user.config.update_profile_every_login and (request.user.profile.image != "default.jpeg") and (
                data["avatar_url"] is not None):
            os.remove(f"media/{request.user.profile.image}")
        if request.user.config.update_profile_every_login and (
                request.user.profile.cover != "default_cover.png") and (data["cover_url"] is not None):
            os.remove(f"media/{request.user.profile.cover}")

        if data["avatar_url"] is not None:
            avatar_pic = requests.get(data["avatar_url"])
            avatar_temp = NamedTemporaryFile(delete=True)
            avatar_temp.write(avatar_pic.content)
            avatar_temp.flush()
            profile.image.save(data["avatar_url"].split('?')[-1], File(avatar_temp), save=True)

        if data["cover_url"] is not None:
            cover_pic = requests.get(data["cover_url"])
            cover_temp = NamedTemporaryFile(delete=True)
            cover_temp.write(cover_pic.content)
            cover_temp.flush()
            profile.cover.save(data["cover_url"].split('/')[-1], File(cover_temp), save=True)

        profile.osu_username = data["username"]
        profile.oauth_first_migrate = True
        profile.save()
    else:
        profile.oauth_first_migrate = True
        profile.save()
