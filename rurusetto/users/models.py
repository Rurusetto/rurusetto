from django.contrib.auth.models import User
from django.contrib.sitemaps import ping_google
from django.core.validators import FileExtensionValidator
from django.db import models
from PIL import Image
from colorfield.fields import ColorField

THEME = (
    # Setting choice for changing theme in website.
    # The in-system value will use as the class name in <body> tag in render template
    # to indicate that what theme user set. (Default is dark mode)
    # In-system value - Show value
    ('', 'Dark Mode (Default)'),
    ('light', 'Light Mode'),
    # ('sync', 'Sync With System Settings')
)

SUBPAGE_INDEX = (
    # Setting for subpage design
    # In-system value - Show value
    ('button', 'Button (Default)'),
    ('list', 'List with expandable accordance'),
)


class Profile(models.Model):
    """
    A model to collect all user's profile related that cannot save in default Django user account model.

    - user: A user that is bind or own this Profile object.
    - image: User's profile picture
    - cover: Cover image in user's profile page.
    - about_me: A text field to introduce yourself or something. It's show at profile page below the username
    - osu_username: User's osu! account username. If this user is signed up with osu! account this field will automatically set from osu! API in user_update_information_in_allauth signal.
    - oauth_first_migrate: This field will tell system that is this user's profile is migrated from osu! account? This value will changed by the system.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tag = models.CharField(default='', max_length=100, blank=True)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics', validators=[FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg', 'webp'])])
    cover = models.ImageField(default='default_cover.png', upload_to='cover_pics', validators=[FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg', 'webp'])])
    about_me = models.TextField(default='Hello there!', max_length=120, blank=True)
    osu_username = models.CharField(default='', max_length=50, blank=True)
    oauth_first_migrate = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            ping_google()
        except Exception:
            pass
        # Use pillow to resize profile image and cover image
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.image.path)
        cover = Image.open(self.cover.path)
        if cover.height > 1080 or cover.width > 1920:
            cover.thumbnail((1920, 1080))
            cover.save(self.cover.path)


class Config(models.Model):
    """
    A model to collect all user's website config for personalization.

    - user: A user that is bind or own this Profile object.
    - update_profile_every_login: This setting will set by user. If this is True, when user login the system will be update user's profile every user's login session by user_update_information_in_allauth signal.
    - theme: Theme of website that user choose. Will choose from THEME variable choice.
    - subpage_index: Design of subpage index in wiki page. WIll choose from SUBPAGE_INDEX variable choice.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    update_profile_every_login = models.BooleanField(default=False)
    theme = models.TextField(choices=THEME, default='')
    subpage_index = models.TextField(choices=SUBPAGE_INDEX, default='button')

    def __str__(self):
        return f'{self.user.username} Config'


class Tag(models.Model):
    """
    A model to collect a tag that use to make a tag for showing in profile page.

    - name: A tag name to display on tag panel of profile page.
    - color: Color of tag when display on profile page
    """
    name = models.CharField(default="Default tag", max_length=25)
    pills_color = ColorField(default="#FF66AA")
    font_color = ColorField(default="#FFFFFF")
    description = models.CharField(default="", max_length=200)

