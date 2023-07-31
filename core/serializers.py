import re
from abc import abstractmethod

from . import models
from . import fields
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class PeopleExtendedBriefSerializer(serializers.Serializer):
    """
    Serializer to send a response back to user.
    This one is a brief version of the serializer, returning only the most important fields
    """

    id = serializers.IntegerField()
    fullname_en = serializers.CharField()
    fullname_ru = serializers.CharField()
    fullname_uk = serializers.CharField(allow_blank=True, allow_null=True)
    dob = serializers.DateField(allow_null=True)
    dod = serializers.DateField(allow_null=True)
    photo = serializers.CharField(allow_blank=True, allow_null=True)
    thumb = serializers.CharField(allow_blank=True, allow_null=True)
    sex = serializers.CharField(allow_blank=True, allow_null=True)

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
            'fullname_en',
            'fullname_ru',
            'fullname_uk',
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
    fullname_en = serializers.CharField()
    fullname_ru = serializers.CharField()
    fullname_uk = serializers.CharField(allow_blank=True, allow_null=True)
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
            'fullname_en',
            'fullname_ru',
            'fullname_uk'
        )


class PeopleExtendedSerializer(serializers.Serializer):
    """
    Full serializer to return almost all fields
    """
    id = serializers.IntegerField()
    fullname_uk = serializers.CharField(allow_blank=True, allow_null=True)
    fullname_en = serializers.CharField()
    fullname_ru = serializers.CharField()
    lastname_en = serializers.CharField(allow_blank=True, allow_null=True)
    lastname_ru = serializers.CharField(allow_blank=True, allow_null=True)
    social = serializers.CharField(allow_blank=True, allow_null=True)
    # social = serializers.ListField(child=serializers.CharField(allow_blank=True, allow_null=True))
    dob = serializers.DateField(allow_null=True)
    is_ttu = serializers.BooleanField(allow_null=True)
    is_ff = serializers.BooleanField(allow_null=True)
    contact = serializers.JSONField(allow_null=True)
    address = serializers.CharField(allow_blank=True, allow_null=True)
    # address = serializers.ListField(child=serializers.CharField(allow_blank=True, allow_null=True))
    associates = serializers.JSONField(allow_null=True)
    # associates = serializers.ListField(child=serializers.JSONField(allow_blank=True, allow_null=True))
    additional = serializers.JSONField(allow_null=True)
    aliases = serializers.JSONField(allow_null=True)
    # aliases = serializers.ListField(child=serializers.JSONField(allow_blank=True, allow_null=True))
    info = serializers.JSONField(allow_null=True)
    dod = serializers.DateField(allow_null=True)
    cod = serializers.CharField(allow_blank=True, allow_null=True)
    known_for = serializers.JSONField(allow_null=True)
    wiki_ref = serializers.JSONField(allow_null=True)
    photo = serializers.CharField(allow_blank=True, allow_null=True)
    external_links = serializers.CharField(allow_blank=True, allow_null=True)
    bundles = serializers.JSONField(allow_null=True)
    # bundles = serializers.ListField(child=serializers.JSONField(allow_blank=True, allow_null=True))
    thumb = serializers.CharField(allow_blank=True, allow_null=True)
    added_on = serializers.DateTimeField(allow_null=False)
    sex = serializers.CharField(allow_null=True)
    orgs = serializers.JSONField(allow_null=True)
    # orgs = serializers.ListField(child=serializers.JSONField(allow_blank=True, allow_null=True))
    telegram_channels = serializers.JSONField(allow_null=True)
    # telegram_channels = serializers.ListField(child=serializers.JSONField(allow_blank=True, allow_null=True))
    youtube_channels = serializers.JSONField(allow_null=True)
    # youtube_channels = serializers.ListField(child=serializers.JSONField(allow_blank=True, allow_null=True))

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
            'fullname_en',
            'fullname_ru',
            'fullname_uk',
            'dob',
            'photo',
            'thumb',
            'social',
            'is_ttu',
            'is_ff',
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
    name_en = serializers.CharField()
    name_ru = serializers.CharField()
    name_uk = serializers.CharField(allow_blank=True, allow_null=True)
    parent_org = serializers.IntegerField(allow_null=True)
    region = serializers.IntegerField(allow_null=True)
    source_url = serializers.CharField(allow_blank=True, allow_null=True)
    org_type = serializers.IntegerField(allow_null=True)
    coverage_type = serializers.IntegerField(allow_null=True)
    short_name = serializers.JSONField(allow_null=True)
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
            'name_en': instance.name_en,
            'name_ru': instance.name_ru,
            'name_uk': instance.name_uk,
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
            'name_en',
            'name_ru',
            'name_uk',
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


class PeopleInOrgsSerializer(serializers.Serializer):
    """
    Serializer for model PeopleInOrgs
    """
    id = serializers.IntegerField()
    org = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(allow_null=True)
    media_segment = serializers.IntegerField(allow_null=True)
    notes = serializers.CharField(allow_blank=True, allow_null=True)
    is_in_control = serializers.BooleanField(allow_null=True)
    role = serializers.JSONField(allow_null=True)
    year_started = serializers.IntegerField(allow_null=True)
    year_ended = serializers.IntegerField(allow_null=True)

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
        model = models.PeopleInOrgs
        fields = (
            'id',
            'org',
            'is_active',
            'media_segment',
            'notes',
            'is_in_control',
            'role',
            'year_started',
            'year_ended'
        )


class CommonRequestSerializer(serializers.Serializer):

    @abstractmethod
    def validate_type(self, value):
        """
        Abstract method for validating the "type" field
        Each concrete subclass must implement this method
        """
        raise NotImplementedError('You must implement `validate_type()` in a subclass')

    def update(self, instance, validated_data):
        """
        We do not manage the update of the data
        """
        pass

    def create(self, validated_data):
        """
        We do not manage the creation of the data
        """
        pass

    @staticmethod
    def tristate_param(param):
        """
        Convert a parameter to tristate value (True, False, None)
        """
        if param is None:
            return None
        if isinstance(param, bool):
            return param
        if isinstance(param, str) and param.lower() in ['true', 'false']:
            return param.lower() == 'true'
        raise ValueError(f'Invalid tristate value [{param}]')


# noinspection PyMethodMayBeStatic
class PagingRequestSerializer(CommonRequestSerializer):

    def update(self, instance, validated_data):
        """
        We do not manage the update of the data
        """
        pass

    def create(self, validated_data):
        """
        We do not manage the creation of the data
        """
        pass

    type = serializers.CharField(required=True)
    page = serializers.IntegerField(required=True, min_value=0)
    page_size = serializers.IntegerField(required=True, min_value=9, max_value=100)
    sort_by = serializers.ChoiceField(choices=['id', 'fullname_en', 'fullname_ru', 'fullname_uk', 'dob', 'dod', 'sex'],
                                      required=False,
                                      default='id')
    sort_direction = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')
    filter = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=100)
    alive = serializers.BooleanField(required=False, allow_null=True)

    def validate_type(self, value):
        if value.lower() != 'page':
            raise ValidationError('Invalid request type, "page" expected')
        return value

    def validate_filter(self, value):
        """
        Validate the filter field
        """
        # Allow empty or null value
        if value is None or value.strip() == '':
            return value

        # Use a regular expression to check if the filter is a valid wildcard mask
        # (e.g., "john*", "*smith", "j?hn", etc.)
        valid_wildcard_mask = re.compile(r'^[\w\s*?]+$')

        if not valid_wildcard_mask.match(value):
            raise ValidationError('Invalid filter format: it must be a valid wildcard mask or empty')

        return value

    def validate_alive(self, value):
        """
        Validate the alive field
        """
        return self.tristate_param(value)
