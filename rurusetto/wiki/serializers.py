from rest_framework import serializers
from .models import Ruleset


class RulesetSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Ruleset model for passing the value to the API view
    """
    class Meta:
        model = Ruleset
        fields = ['id', 'name', 'slug', 'description', 'icon', 'logo', 'cover_image', 'opengraph_image', 'source', 'content',
                  'creator', 'owner', 'last_edited_by', 'created_at', 'last_edited_at', 'verified']
