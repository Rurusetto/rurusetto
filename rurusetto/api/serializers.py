from rest_framework import serializers
from wiki.models import Ruleset


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
