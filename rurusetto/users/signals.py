from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Config
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests
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
def user_first_logged_in_allauth(request, user, **kwargs):
    profile = Profile.objects.get(user=request.user)
    if (not profile.oauth_first_migrate) or request.user.config.update_profile_every_login:
        try:
            data = SocialAccount.objects.get(user=request.user).extra_data

            avatar_pic = requests.get(data["avatar_url"])
            avatar_temp = NamedTemporaryFile(delete=True)
            avatar_temp.write(avatar_pic.content)
            avatar_temp.flush()
            profile.image.save(data["avatar_url"].split('?')[-1], File(avatar_temp), save=True)

            cover_pic = requests.get(data["cover_url"])
            cover_temp = NamedTemporaryFile(delete=True)
            cover_temp.write(cover_pic.content)
            cover_temp.flush()
            profile.cover.save(data["cover_url"].split('/')[-1], File(cover_temp), save=True)

            profile.osu_username = data["username"]
            profile.osu_id = data["id"]
            profile.location = data["location"] if data["location"] is not None else ""
            profile.interests = data["interests"] if data["interests"] is not None else ""
            profile.occupation = data["occupation"] if data["occupation"] is not None else ""
            profile.twitter = data["twitter"] if data["twitter"] is not None else ""
            profile.discord = data["discord"] if data["discord"] is not None else ""
            profile.website = data["website"] if data["website"] is not None else ""

            profile.oauth_first_migrate = True
            profile.social_account = True
            profile.save()
        except:
            profile.oauth_first_migrate = True
            profile.social_account = False
            profile.save()

