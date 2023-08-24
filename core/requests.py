import re
from abc import abstractmethod

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


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
        We do not manage the update of the data
        """
        pass

    allowed_fields = ['id', 'fullname_en', 'fullname_ru', 'fullname_uk', 'dob', 'dod', 'sex']
    type = serializers.CharField(required=True)
    page = serializers.IntegerField(required=True, min_value=0)
    page_size = serializers.IntegerField(required=True, min_value=8, max_value=120)
    sort_by = serializers.ChoiceField(choices=allowed_fields, required=False, default='id')
    sort_direction = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')
    filter = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=100)
    alive = serializers.BooleanField(required=False, allow_null=True)
    sex = serializers.ChoiceField(choices=[('M', 'M'), ('F', 'F')], required=False)
    age = serializers.IntegerField(required=False, min_value=1)
    age_direction = serializers.ChoiceField(choices=[('below', 'below'), ('above', 'above')], required=False)
    is_ttu = serializers.BooleanField(required=False)
    is_ff = serializers.BooleanField(required=False)

    def validate_type(self, value):
        if value.lower() != 'page':
            raise ValidationError('Invalid request type, "page" expected')
        return value

    def validate_filter(self, value):
        if value is None or value.strip() == '':
            return value

        valid_wildcard_mask = re.compile(r'^[\w\s*?]+$')

        if not valid_wildcard_mask.match(value):
            raise ValidationError('Invalid filter format: it must be a valid wildcard mask or empty')

        return value

    def validate_alive(self, value):
        return self.tristate_param(value)
