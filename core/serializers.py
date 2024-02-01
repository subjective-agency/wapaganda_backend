from . import models
from . import fields
from rest_framework import serializers


class TripleLangSerializer(serializers.Serializer):
    en = serializers.CharField(allow_null=True)
    ru = serializers.CharField(allow_null=True)
    uk = serializers.CharField(allow_null=True)

    class Meta:
        model = models.TripleLang
        fields = ('en', 'ru', 'uk')


class TheorySerializer(serializers.Serializer):
    """
    Serializer for Theory table, containing relatively large articles
    """
    id = serializers.IntegerField()
    title = TripleLangSerializer()
    type = serializers.CharField(allow_blank=True, allow_null=True)
    excerpt = TripleLangSerializer(allow_null=True)
    content = TripleLangSerializer(allow_null=True)
    original_content_metadata = serializers.JSONField(allow_null=True)
    publish_date = serializers.DateTimeField(allow_null=True)
    images = serializers.CharField(allow_blank=True, allow_null=True)
    added_at = serializers.DateTimeField(allow_null=False)
    translated_by = serializers.JSONField(allow_null=True)
    updated_on = serializers.DateTimeField(allow_null=True)

    def create(self, validated_data):
        """
        We do not manage the creation of the data
        """
        pass

    def update(self, instance, validated_data):
        """
        We do not manage the update of the data
        """
        pass

    class Meta:
        model = models.Theory
        fields = (
            'id',
            'title',
            'type',
            'excerpt',
            'content',
            'original_content_metadata'
            'images',
            'added_at',
            'updated_on',
            'translated_by'
        )


lass AirtimeSerializer(serializers.Serializer):
    episode_id = serializers.IntegerField()
    episode_title = serializers.CharField()
    episode_duration = serializers.IntegerField(allow_null=True)
    episode_date = serializers.DateField()
    media_segment_id = serializers.IntegerField(allow_null=True)
    media_segment_name = TripleLangSerializer(allow_null=True)
    role = serializers.CharField(allow_null=True)

    
class BundleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = TripleLangSerializer()
    bundle_type_id = serializers.IntegerField()
    description = serializers.CharField(allow_null=True)
    updated_on = serializers.DateTimeField(allow_null=True)
    parent_bundle_id = serializers.IntegerField(allow_null=True)

    
class PeopleExtendedBriefSerializer(serializers.Serializer):
    """
    Serializer to send a response back to user.
    This one is a brief version of the serializer, returning only the most important fields
    """

    id = serializers.IntegerField()
    fullname = TripleLangSerializer()
    dob = serializers.DateField(allow_null=True)
    dod = serializers.DateField(allow_null=True)
    photo = serializers.CharField(allow_blank=True, allow_null=True)
    thumb = serializers.CharField(allow_blank=True, allow_null=True)
    sex = serializers.CharField(allow_blank=True, allow_null=True)
    known_for = TripleLangSerializer()

    def create(self, validated_data):
        """
        We do not manage the creation of the data
        """
        pass

    def update(self, instance, validated_data):
        """
        We do not manage the update of the data
        """
        pass

    class Meta:
        model = models.PeopleExtended
        fields = (
            'id',
            'fullname',
            'dob',
            'dod',
            'photo',
            'thumb',
            'sex'
        )


class CacheSerializer(serializers.Serializer):
    """
    Serializer to send a response back to user.
    This one is a brief version of the serializer, returning only the most important fields
    """
    id = serializers.IntegerField()
    fullname = TripleLangSerializer()
    added_on = fields.UnixTimestampField()

    def create(self, validated_data):
        """
        We do not manage the creation of the data
        """
        pass

    def update(self, instance, validated_data):
        """
        We do not manage the update of the data
        """
        pass

    class Meta:
        model = models.PeopleExtended
        fields = (
            'id',
            'fullname',
        )





class PeopleExtendedSerializer(serializers.Serializer):
    """
    Full serializer to return almost all fields
    """
    id = serializers.IntegerField()
    fullname = TripleLangSerializer()
    lastname = TripleLangSerializer()
    social = serializers.CharField(allow_blank=True, allow_null=True)
    dob = serializers.DateField(allow_null=True)
    contact = serializers.JSONField(allow_null=True)
    address = serializers.CharField(allow_blank=True, allow_null=True)
    associates = serializers.JSONField(allow_null=True)
    additional = serializers.JSONField(allow_null=True)
    aliases = TripleLangSerializer(allow_null=True)
    info = TripleLangSerializer()
    dod = serializers.DateField(allow_null=True)
    cod = serializers.CharField(allow_blank=True, allow_null=True)
    known_for = TripleLangSerializer()
    wiki_ref = serializers.JSONField(allow_null=True)
    photo = serializers.CharField(allow_blank=True, allow_null=True)
    external_links = serializers.CharField(allow_blank=True, allow_null=True)
    bundles = serializers.JSONField(allow_null=True)
    thumb = serializers.CharField(allow_blank=True, allow_null=True)
    added_on = serializers.DateTimeField(allow_null=False)
    sex = serializers.CharField(allow_null=True)
    orgs = serializers.JSONField(allow_null=True)
    telegram_channels = serializers.JSONField(allow_null=True)
    youtube_channels = serializers.JSONField(allow_null=True)

    def create(self, validated_data):
        """
        We do not manage the creation of the data
        """
        pass

    def update(self, instance, validated_data):
        """
        We do not manage the update of the data
        """
        pass

    class Meta:
        model = models.PeopleExtended
        fields = (
            'id',
            'fullname',
            'dob',
            'photo',
            'thumb',
            'social',
            'contact',
            'address',
            'associates',
            'additional',
            'aliases',
            'info',
            'dod',
            'cod',
            'known_for',
            'wiki_ref',
            'added_on',
            "sex",
            "orgs",
            "telegram_channels",
            "youtube_channels"
        )


class OrganizationSerializer(serializers.Serializer):
    """
    Serializer for model Organizations
    """
    id = serializers.IntegerField()
    name = TripleLangSerializer()
    parent_org = serializers.IntegerField(allow_null=True)
    region = serializers.IntegerField(allow_null=True)
    source_url = serializers.CharField(allow_blank=True, allow_null=True)
    org_type = serializers.IntegerField(allow_null=True)
    coverage_type = serializers.IntegerField(allow_null=True)
    short_name = TripleLangSerializer()
    state_affiliated = serializers.BooleanField(allow_null=True)
    org_form_raw = serializers.CharField(allow_blank=True, allow_null=True)
    org_form = serializers.JSONField(allow_null=True)
    international = serializers.BooleanField(allow_null=True)
    relevant = serializers.BooleanField()

    def create(self, validated_data):
        """
        We do not manage the creation of the data
        """
        pass

    def update(self, instance, validated_data):
        """
        We do not manage the update of the data
        """
        pass

    def to_representation(self, instance):
        # create a dictionary with the fields to be serialized
        representation = {
            'id': instance.id,
            'name': instance.name,
            'parent_org': instance.parent_org,
            'region': instance.region,
            'source_url': instance.source_url,
            'org_type': instance.org_type,
            'coverage_type': instance.coverage_type,
            'short_name': instance.short_name,
            'state_affiliated': instance.state_affiliated,
            'org_form_raw': instance.org_form_raw,
            'org_form': instance.org_form,
            'international': instance.international,
            'relevant': instance.relevant,
        }
        return representation

    class Meta:
        model = models.Organizations
        fields = (
            'id',
            'name',
            'parent_org',
            'region',
            'source_url',
            'org_type',
            'coverage_type',
            'short_name',
            'state_affiliated',
            'org_form_raw',
            'org_form',
            'international',
            'relevant'
        )
