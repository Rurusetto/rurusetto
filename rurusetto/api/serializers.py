from rest_framework import serializers
from wiki.models import Ruleset
from users.models import Profile
from django.contrib.auth.models import User


class RulesetSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Ruleset model for passing the value to the API view
    """
    class Meta:
        model = Ruleset
        fields = ['id', 'name', 'slug', 'description', 'icon', 'light_icon', 'logo', 'cover_image', 'cover_image_light',
                  'opengraph_image', 'recommend_beatmap_cover', 'custom_css', 'content', 'source', 'github_download_filename',
                  'creator', 'created_at', 'owner', 'last_edited_at', 'last_edited_by', 'verified', 'archive']


class MinimizeRulesetSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Ruleset model for passing only main detail of the ruleset to the API view
    """
    class Meta:
        model = Ruleset
        fields = ['id', 'name', 'slug', 'description', 'icon', 'light_icon', 'source', 'github_download_filename',
                  'owner', 'verified', 'archive']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


# Serializer for listing page


class ProfileListingSerializer(serializers.ModelSerializer):
    """
    Serializer that will only filter the profile of owner to use in RulesetListingSerializer.
    """
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'image']
        depth = 1


class RulesetListingSerializer(serializers.ModelSerializer):
    """
    Serializer for essential information that is user in listing page.
    """
    owner_detail = serializers.SerializerMethodField()

    class Meta:
        model = Ruleset
        fields = ['id', 'name', 'slug', 'description', 'icon', 'light_icon', 'owner_detail']

    def get_owner_detail(self, obj):
        owner = Profile.objects.get(id=obj.owner)
        return ProfileListingSerializer(owner).data
