from . import models
from rest_framework import serializers


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
    photo = serializers.CharField(allow_blank=True, allow_null=True)
    thumb = serializers.CharField(allow_blank=True, allow_null=True)

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
            'thumb'
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
    dob = serializers.DateField(allow_null=True)
    is_ttu = serializers.BooleanField(allow_null=True)
    is_ff = serializers.BooleanField(allow_null=True)
    contact = serializers.JSONField(allow_null=True)
    address = serializers.CharField(allow_blank=True, allow_null=True)
    associates = serializers.CharField(allow_blank=True, allow_null=True)
    additional = serializers.JSONField(allow_null=True)
    aliases = serializers.CharField(allow_blank=True, allow_null=True)
    info = serializers.JSONField(allow_null=True)
    dod = serializers.DateField(allow_null=True)
    cod = serializers.CharField(allow_blank=True, allow_null=True)
    known_for = serializers.JSONField(allow_null=True)
    wiki_ref = serializers.JSONField(allow_null=True)
    photo = serializers.CharField(allow_blank=True, allow_null=True)
    external_links = serializers.CharField(allow_blank=True, allow_null=True)
    bundles = serializers.JSONField(allow_null=True)
    thumb = serializers.CharField(allow_blank=True, allow_null=True)

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
            'wiki_ref'
        )
