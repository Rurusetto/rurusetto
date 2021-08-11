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
    if created:
        Profile.objects.create(user=instance)
        Config.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(user_logged_in, dispatch_uid="unique")
def user_update_information_in_allauth(request, user, **kwargs):
    profile = Profile.objects.get(user=request.user)
    try:
        if (not profile.oauth_first_migrate) or request.user.config.update_profile_every_login:
            data = SocialAccount.objects.get(user=request.user).extra_data

            # If extra data from user detail from osu! API is not None (null in JSON) and it's not default image, can delete
            if request.user.config.update_profile_every_login and (request.user.profile.image != "default.jpeg") and (data["avatar_url"] is not None):
                os.remove(f"media/{request.user.profile.image}")

            if request.user.config.update_profile_every_login and (request.user.profile.cover != "default_cover.png") and (data["cover_url"] is not None):
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
            profile.osu_id = data["id"]

            if data["location"] is None:
                profile.location = ""
            else:
                profile.location = data["location"]

            if data["interests"] is None:
                profile.interests = ""
            else:
                profile.interests = data["interests"]

            if data["occupation"] is None:
                profile.occupation = ""
            else:
                profile.occupation = data["occupation"]

            if data["twitter"] is None:
                profile.twitter = ""
            else:
                profile.twitter = data["twitter"]

            if data["discord"] is None:
                profile.discord = ""
            else:
                profile.discord = data["discord"]

            if data["website"] is None:
                profile.website = ""
            else:
                profile.website = data["website"]

            profile.oauth_first_migrate = True
            profile.social_account = True
            profile.save()
    except:
        profile.oauth_first_migrate = True
        profile.social_account = False
        profile.save()

