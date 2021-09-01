from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from .models import Changelog, Ruleset
from .views import changelog

# Create your tests here.


class ChangelogModelTest(TestCase):

    def test_changelog_model(self):
        """Test that Changelog value are correct when create."""
        Changelog.objects.create(version="AwesomeUpdate", type="stable", note="Update is here!")
        Changelog.objects.create(version="PreReleaseUpdate", type="pre-release", note="Try this update!")
        awesome_update = Changelog.objects.get(version="AwesomeUpdate")
        pre_release_update = Changelog.objects.get(version="PreReleaseUpdate")
        # Test that the value in Changelog object that just create is equal.
        self.assertEqual(awesome_update.version, "AwesomeUpdate")
        self.assertEqual(awesome_update.type, "stable")
        self.assertEqual(awesome_update.note, "Update is here!")
        self.assertEqual(pre_release_update.version, "PreReleaseUpdate")
        self.assertEqual(pre_release_update.type, "pre-release")
        self.assertEqual(pre_release_update.note, "Try this update!")
    
    def test_changelog_default_value(self):
        """Test that value if we don't put anything to Changelog model it will use a valid default value from model."""
        Changelog.objects.create(id=3)
        default_changelog = Changelog.objects.get(id=3)
        # Test that value are equal to default value.
        self.assertEqual(default_changelog.version, '')
        self.assertEqual(default_changelog.type, 'stable')


class ChangelogViewTest(TestCase):

    def test_access_changelog_page(self):
        """Test that everyone can access Changelog page."""
        factory = RequestFactory()
        user = User.objects.create_user(username="Pippi", email="pippi@peppy.com", password="cookiezilnwza")

        # Create an instance of a GET request.
        request = factory.get('/changelog')
        request.user = user
        response = changelog(request)
        self.assertEquals(response.status_code, 200)
        request.user = AnonymousUser()
        response = changelog(request)
        self.assertEquals(response.status_code, 200)


class RulesetModelTest(TestCase):

    def test_ruleset_model(self):
        """Test that Ruleset value are correct when create."""
        Ruleset.objects.create(creator='5', owner='5', name='Awesome Ruleset', slug='awesome-ruleset',
                               description='Best ruleset', icon='default_icon.png', logo='default_logo.jpeg',
                               cover_image='default_wiki_cover.jpeg', opengraph_image='default_wiki_cover.jpeg',
                               recommend_beatmap_cover='default_recommend_beatmap_cover.png', content='osu! and everything',
                               source='https://www.github.com/ppy/osu', last_edited_by='5', verified=False)
        test_ruleset = Ruleset.objects.get(name='Awesome Ruleset')
        # Test that the value in Ruleset object that just create is equal.
        # TODO: Add test image
        self.assertEqual(test_ruleset.creator, '5')
        self.assertEqual(test_ruleset.owner, '5')
        self.assertEqual(test_ruleset.name, 'Awesome Ruleset')
        self.assertEqual(test_ruleset.slug, 'awesome-ruleset')
        self.assertEqual(test_ruleset.description, 'Best ruleset')
        self.assertEqual(test_ruleset.icon, 'default_icon.png')
        self.assertEqual(test_ruleset.logo, 'default_logo.jpeg')
        self.assertEqual(test_ruleset.cover_image, 'default_wiki_cover.jpeg')
        self.assertEqual(test_ruleset.opengraph_image, 'default_wiki_cover.jpeg')
        self.assertEqual(test_ruleset.recommend_beatmap_cover, 'default_recommend_beatmap_cover.png')
        self.assertEqual(test_ruleset.content, 'osu! and everything')
        self.assertEqual(test_ruleset.source, 'https://www.github.com/ppy/osu')
        self.assertEqual(test_ruleset.last_edited_by, '5')
        self.assertEqual(test_ruleset.verified, False)

    def test_ruleset_default_value(self):
        """Test that value if we don't put anything to Ruleset model it will use a valid default value from model."""
        Ruleset.objects.create(id=2)
        blank_ruleset = Ruleset.objects.get(id=2)
        # Test that value are equal to default value.
        self.assertEqual(blank_ruleset.creator, '0')
        self.assertEqual(blank_ruleset.owner, '0')
        self.assertEqual(blank_ruleset.name, '')
        self.assertEqual(blank_ruleset.slug, '')
        self.assertEqual(blank_ruleset.description, '')
        self.assertEqual(blank_ruleset.icon, 'default_icon.png')
        self.assertEqual(blank_ruleset.logo, 'default_logo.jpeg')
        self.assertEqual(blank_ruleset.cover_image, 'default_wiki_cover.jpeg')
        self.assertEqual(blank_ruleset.opengraph_image, 'default_wiki_cover.jpeg')
        self.assertEqual(blank_ruleset.recommend_beatmap_cover, 'default_recommend_beatmap_cover.png')
        self.assertEqual(blank_ruleset.content, '')
        self.assertEqual(blank_ruleset.source, '')
        self.assertEqual(blank_ruleset.last_edited_by, '0')
        self.assertEqual(blank_ruleset.verified, False)

