from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from mdeditor.fields import MDTextField
from django.contrib.sitemaps import ping_google
from PIL import Image

RELEASE_TYPE = (
    # In-system value - Show value
    ('pre-release', 'Pre-release'),
    ('stable', 'Stable')
)


class Changelog(models.Model):
    """
    A model to collect an update changelog in changelog page.

    - version: A version name of that changelog version
    - time: The time that changelog added. Will add automatically on save.
    - type: Type of that version (pre-release or stable). Select by choice.
    - note: Changelog detail
    """
    version = models.CharField(default='', max_length=30)
    time = models.DateTimeField(auto_now_add=True)
    type = models.TextField(choices=RELEASE_TYPE, default='stable')
    note = MDTextField()

    def __str__(self):
        return f'{self.version} changelog ({self.type})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            ping_google()
        except Exception:
            pass


class Ruleset(models.Model):
    """
    A model of a ruleset and the front page of each ruleset wiki.

    - creator: A user ID who create this page (This field is based on the case that the ruleset owner
    is not add a ruleset themselves.
    - owner: A user ID of the ruleset owner. This field when create the ruleset
    it will assign the creator user ID but the wiki maintainer will change it to a real owner later.
    - name: A ruleset name
    - slug: A slug of ruleset name. This value will always regenerate when the ruleset name is saved and
    it will use as a URL to ruleset page.
    - description: A ruleset description that is show on the listing page.
    - icon: An icon is a circle image that is show at in-game header. Recommend shape is circle.
    - logo: A logo will show in wiki's infobox. It can be not same to an icon.
    - cover_image: A picture at the header of the wiki page.
    - opengraph_image: An image that is show on the the opengraph when link to the ruleset URL
    - recommend_beatmap_cover: An image that use on a header of recommend beatmap page of that ruleset.
    - content: A content of an index page.
    - source: A source of the ruleset (or where the player can download this ruleset.)
    - last_edited_by: A user ID of who is the latest edit this ruleset.
    - last_edited_at: A time that this ruleset is latest edit. Will auto assign when it's save.
    - created_at: A time that this ruleset was created.
    - verified: A boolean that will change to True by the wiki maintainer when the wiki maintainer is already
    verified that the owner is right. When this value is True, on the ruleset owner name will have a pink tick at
    the creator's username on that page. The default value is False.
    """
    creator = models.CharField(default="0", max_length=10)
    owner = models.CharField(default="0", max_length=10)

    name = models.CharField(default="", max_length=20)
    slug = models.SlugField(default="", max_length=20)
    description = models.CharField(default="", max_length=150)
    icon = models.ImageField(default='default_icon.png', upload_to='rulesets_icon', validators=[
        FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg', 'webp'])])
    logo = models.ImageField(default='default_logo.jpeg', upload_to='rulesets_logo', validators=[
        FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg', 'webp'])])
    cover_image = models.ImageField(default='default_wiki_cover.jpeg', upload_to='wiki_cover', validators=[
        FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg', 'webp'])])
    opengraph_image = models.ImageField(default='default_wiki_cover.jpeg', upload_to='rulesets_opengraph_image', validators=[
        FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg', 'webp'])])
    recommend_beatmap_cover = models.ImageField(default='default_recommend_beatmap_cover.png', upload_to='recommend_beatmap_cover', validators=[
        FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg', 'webp'])])

    content = MDTextField()

    source = models.URLField(default="")

    last_edited_by = models.CharField(default="0", max_length=10)
    last_edited_at = models.DateTimeField(auto_now=True, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            ping_google()
        except Exception:
            pass
        # Use pillow to resize cover_image, opengraph_image, recommend_beatmap
        img = Image.open(self.cover_image.path)
        if img.height > 1080 or img.width > 1920:
            img.thumbnail((1920, 1080))
            img.save(self.cover_image.path)
        opengraph = Image.open(self.opengraph_image.path)
        if opengraph.height > 1080 or opengraph.width > 1920:
            opengraph.thumbnail((1920, 1080))
            opengraph.save(self.opengraph_image.path)
        recommend_beatmap = Image.open(self.recommend_beatmap_cover.path)
        if recommend_beatmap.height > 1080 or recommend_beatmap.width > 1920:
            recommend_beatmap.thumbnail((1920, 1080))
            recommend_beatmap.save(self.recommend_beatmap_cover.path)


class Subpage(models.Model):
    """
    A model to contain the subpage of the main ruleset wiki.

    - ruleset_id: The ID of ruleset model that this subpage is bind to.
    - title: Title of subpage
    - slug: Slug of subpage title. This value will always regenerate when the subpage title is saved and
    it will use as a URL to this subpage page.
    - content: Content of the subpage page.
    - creator: A user ID of subpage creator or who create this subpage.
    - last_edited_by: A user ID of who is the latest edit this subpage.
    - last_edited_at: A time that this subpage is latest edit. Will auto assign when it's save.
    - created_at: A time that this subpage was created.
    """
    ruleset_id = models.CharField(default="0", max_length=10)

    title = models.CharField(default="", max_length=50)
    slug = models.SlugField(default="", max_length=50)

    content = MDTextField()

    creator = models.CharField(default="0", max_length=10)
    last_edited_by = models.CharField(default="0", max_length=10)
    last_edited_at = models.DateTimeField(auto_now=True, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} (Subpage of {Ruleset.objects.get(id=int(self.ruleset_id)).name})'


class RecommendBeatmap(models.Model):
    """
    A model to contain the beatmap in recommend beatmaps section in each ruleset.

    In this model user mainly fill only 2 fields from recommend beatmap form:

    - beatmap_id: Beatmap ID that user fill in when user add a recommend beatmap form.
    - comment: Short comment why this user recommend this beatmap.

    Other fields are auto-import by the form view and the data of these field are from osu! API.
    The default value come from beatmap name DISCO PRINCE by peppy.
    These field name are set to make it same as osu! API field name.

    - ruleset_id: ID of ruleset model that this beatmap is bind to.
    - user_id: A user ID who create this object.
    - beatmapset_id: ID of set of beatmap that this beatmap is in.
    - title: Beatmap name. (Or beatmapset name)
    - artist: Song artist of the beatmap.
    - source: Source of song in beatmap.
    - creator: A creator osu! username who make this beatmap.
    - approved: A status of beatmap. (4 = Loved, 3 = Qualified, 2 = Approved, 1 = Ranked, 0 = Pending, -1 = WIP, -2 = Graveyard)
    - difficultyrating: A star rating or SR of the beatmap.
    - bpm: BPM of the song in beatmap. The data from osu! is mainly come in 6-digits float.
    - version: A beatmap name of this beatmap.
    - URL: An URL to open this beatmap in osu! website.
    - beatmap_cover: An image of the beatmap cover image.
    - beatmap_thumbnail: An image of beatmap thumbnail.
    - created_at: A time that this beatmap was created.
    """
    ruleset_id = models.CharField(default="0", max_length=10)
    user_id = models.CharField(default="0", max_length=10)

    beatmap_id = models.IntegerField(default=75)
    beatmapset_id = models.IntegerField(default=1)

    title = models.CharField(default="DISCO PRINCE", max_length=100)
    artist = models.CharField(default="Kenji Ninuma", max_length=100)
    source = models.CharField(default="", max_length=100)
    creator = models.CharField(default="peppy", max_length=100)
    approved = models.CharField(default="1", max_length=10)
    difficultyrating = models.FloatField(default="2.39774")
    bpm = models.CharField(default="119.999", max_length=10)
    version = models.CharField(default="Normal", max_length=50)

    url = models.URLField(default="https://osu.ppy.sh/beatmapsets/1#osu/75")

    beatmap_cover = models.ImageField(default='default_beatmap_cover.jpeg', upload_to='beatmap_cover', validators=[
        FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg', 'webp'])])
    beatmap_thumbnail = models.ImageField(default='default_beatmap_thumbnail.jpeg', upload_to='beatmap_thumbnail', validators=[
        FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg', 'webp'])])

    comment = models.CharField(default=None, max_length=150)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} [{self.version}] (Recommend of {Ruleset.objects.get(id=int(self.ruleset_id)).name})'


class CustomWiki(models.Model):
    title = models.CharField(default="", max_length=100)

    time = models.DateTimeField(auto_now_add=True)
    last_edited_at = models.DateTimeField(auto_now=True, editable=True)

    creator = models.CharField(default="0", max_length=10)
    last_edited_by = models.CharField(default="0", max_length=10)

    content = MDTextField()

    def __str__(self):
        return f'{self.version} changelog ({self.type})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            ping_google()
        except Exception:
            pass