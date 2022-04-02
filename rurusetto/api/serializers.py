from rest_framework import serializers
from wiki.models import Ruleset, Subpage, RulesetStatus
from users.models import Profile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileMiniSerializer(serializers.ModelSerializer):
    """
    Serializer that will only filter the profile of owner to use in RulesetListingSerializer.
    """
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'image']
        depth = 1


# Serializer for listing page


class RulesetListingSerializer(serializers.ModelSerializer):
    """
    Serializer for essential information that is user in listing page.
    """
    owner_detail = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Ruleset
        fields = ['id', 'name', 'slug', 'description', 'icon', 'light_icon', 'owner_detail', 'verified', 'archive',
                  'direct_download_link', 'can_download', 'status']

    def get_owner_detail(self, obj):
        try:
            owner = Profile.objects.get(id=obj.owner)
            return ProfileMiniSerializer(owner).data
        except Profile.DoesNotExist:
            return {}

    def get_status(self, obj):
        try:
            return StatusDetailSerializer(RulesetStatus.objects.get(ruleset=obj)).data
        except RulesetStatus.DoesNotExist:
            return {}


# Serializer for rulesets detail


class StatusDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Status model that use in RulesetsDetailSerializer
    """
    class Meta:
        model = RulesetStatus
        fields = ['latest_version', 'latest_update', 'pre_release', 'changelog', 'file_size', 'playable']


class RulesetsDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for essential information in wiki view of each rulesets
    """
    creator_detail = serializers.SerializerMethodField()
    owner_detail = serializers.SerializerMethodField()
    last_edited_by_detail = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Ruleset
        fields = ['id', 'name', 'slug', 'description', 'icon', 'light_icon', 'logo', 'cover_image', 'cover_image_light',
                  'opengraph_image', 'custom_css', 'content', 'source',
                  'github_download_filename', 'direct_download_link', 'can_download', 'creator_detail', 'created_at', 'owner_detail',
                  'last_edited_at', 'last_edited_by_detail', 'verified', 'archive', 'status']

    def get_creator_detail(self, obj):
        try:
            return ProfileMiniSerializer(Profile.objects.get(id=obj.creator)).data
        except Profile.DoesNotExist:
            return {}

    def get_owner_detail(self, obj):
        try:
            return ProfileMiniSerializer(Profile.objects.get(id=obj.owner)).data
        except Profile.DoesNotExist:
            return {}

    def get_last_edited_by_detail(self, obj):
        try:
            return ProfileMiniSerializer(Profile.objects.get(id=obj.last_edited_by)).data
        except Profile.DoesNotExist:
            return {}

    def get_status(self, obj):
        try:
            return StatusDetailSerializer(RulesetStatus.objects.get(ruleset=obj)).data
        except RulesetStatus.DoesNotExist:
            return {}

# Serializer for subpoge

class RulesetsSubpageSerializer(serializers.ModelSerializer):
    """
    Serializer for Subpage model to get only detail that use in rulesets
    """
    class Meta:
        model = Subpage
        fields = ['title', 'slug']


class SubpageSerializer(serializers.ModelSerializer):
    """
    Serializer for Subpage model to get full detail of subpage
    """
    ruleset_detail = serializers.SerializerMethodField()
    last_edited_by_detail = serializers.SerializerMethodField()
    creator_detail = serializers.SerializerMethodField()

    class Meta:
        model = Subpage
        fields = ['ruleset_detail', 'title', 'slug', 'content', 'creator_detail', 'last_edited_by_detail', 'last_edited_at',
                  'created_at']

    def get_ruleset_detail(self, obj):
        try:
            return RulesetListingSerializer(Ruleset.objects.get(id=obj.ruleset_id)).data
        except Ruleset.DoesNotExist:
            return {}

    def get_creator_detail(self, obj):
        try:
            return ProfileMiniSerializer(Profile.objects.get(id=obj.creator)).data
        except Profile.DoesNotExist:
            return {}

    def get_last_edited_by_detail(self, obj):
        try:
            return ProfileMiniSerializer(Profile.objects.get(id=obj.last_edited_by)).data
        except Profile.DoesNotExist:
            return {}


# Serializer for user and profile

class UserFullSerializer(serializers.ModelSerializer):
    """
    Serializer for full detail of users
    """
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'image', 'cover', 'cover_light', 'about_me', 'osu_username']
        depth = 1
