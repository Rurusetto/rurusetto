from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from .models import Changelog
from .views import changelog

# Create your tests here.


class ChangelogModelTest(TestCase):

    def test_changelog_model(self):
        """Test that Changelog value are correct"""
        Changelog.objects.create(version="AwesomeUpdate", type="stable", note="Update is here!")
        Changelog.objects.create(version="PreReleaseUpdate", type="pre-release", note="Try this update!")
        awesome_update = Changelog.objects.get(version="AwesomeUpdate")
        pre_release_update = Changelog.objects.get(version="PreReleaseUpdate")
        # Test that the value in model object that just create is equal.
        self.assertEqual(awesome_update.version, "AwesomeUpdate")
        self.assertEqual(awesome_update.type, "stable")
        self.assertEqual(awesome_update.note, "Update is here!")
        self.assertEqual(pre_release_update.version, "PreReleaseUpdate")
        self.assertEqual(pre_release_update.type, "pre-release")
        self.assertEqual(pre_release_update.note, "Try this update!")


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