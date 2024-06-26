import re
from abc import abstractmethod
from datetime import datetime

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
        if isinstance(param, int) and param in (0, 1):
            return bool(param)
        if isinstance(param, str) and param.lower() in ['true', 'false']:
            return param.lower() == 'true'
        raise ValueError(f'Invalid tristate value [{param}]')


# noinspection PyMethodMayBeStatic
class PagingRequestSerializer(CommonRequestSerializer):
    """
    Filters:
    * Alive: If the value `alive: true` or `alive: false` is defined, we perform the respective query.
      In other words, if we define `alive: true`, we return only alive people, if `alive: false`,
      we return only dead people, if we don't define `alive`, we return everyone.
    # * Traitor to Ukraine: If the value `is_ttu: true` or `is_ttu: false` is defined, we perform the respective query.
    #   If undefined, we return everyone
    # * Foreign Friend: If the value `is_ff: true` or `is_ff: false` is defined, we perform the respective query.
    #   If undefined, we return everyone
    * Sex (gender): If the value `sex: "M"` or `sex: "F"` is defined, we perform the respective query.
      If undefined, we return both men and women
    * Full name: If the filter value in wildcard format is defined, we perform the respective query.
      E.g. `"filter": "Ivan*"` will return all people whose full name starts with "Ivan"
      If undefined, we return everyone
    * Age: If values age_min: N1 and age_max: N2 are defined, we request the respective age range.
      If only value age_min: N is defined, we request all ages above.
      If only value age_max: N is defined, we request all ages below.
      If undefined, we return everyone

    In the end we apply the sorting condition, then requests paginated data from a sorted dataset
    E.g. 11th page with page size 20 returns records 200-220.
    Default sort_by value is "fullname_en", sort_direction is "asc" order
    """

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

    allowed_fields = ['id', 'fullname', 'lastname']
    type = serializers.CharField(required=True)
    page = serializers.IntegerField(required=True, min_value=0)
    page_size = serializers.IntegerField(required=True, min_value=8, max_value=120)
    sort_by = serializers.ChoiceField(choices=allowed_fields, required=False, default='id')
    sort_direction = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')
    filter = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=100)
    sex = serializers.ChoiceField(choices=[('m', 'm'), ('f', 'f')], required=False, allow_null=True)
    age_min = serializers.IntegerField(required=False, min_value=1, max_value=99, allow_null=True)
    age_max = serializers.IntegerField(required=False, min_value=1, max_value=99, allow_null=True)
    alive = serializers.BooleanField(required=False, allow_null=True)
    flags = serializers.ListField(child=serializers.IntegerField(), required=False, allow_null=True)
    groups = serializers.ListField(child=serializers.IntegerField(), required=False, allow_null=True)
    expertise = serializers.ListField(child=serializers.IntegerField(), required=False, allow_null=True)

    def validate(self, data):
        """
        Custom validation for age_min and age_max
        """
        age_min = data.get('age_min', 1)
        age_max = data.get('age_max', 99)
        age_min = age_min if age_min is not None else 1
        age_max = age_max if age_max is not None else 99
        if age_min > age_max:
            raise ValidationError('age_min should be less than or equal to age_max')
        return data

    def validate_type(self, value):
        """
        Validate the "type" field
        """
        if value.lower() != 'page':
            raise ValidationError('Invalid request type, "page" expected')
        return value

    def validate_filter(self, value):
        """
        Validate the "filter" value to match wildcard mask
        """
        if value is None or value.strip() == '':
            return value

        valid_wildcard_mask = re.compile(r'^[\w\s*?]+$')

        if not valid_wildcard_mask.match(value):
            raise ValidationError('Invalid filter format: it must be a valid wildcard mask or empty')

        return value

    def validate_alive(self, value):
        """
        Convert a parameter to tristate value (True, False, None)
        """
        return self.tristate_param(value)

    def validate_flags(self, value):
        """
        Validate the "flags" field.
        """
        if value is not None:
            if not isinstance(value, list):
                raise ValidationError('Flags must be a list of integers')
            if not all(isinstance(item, int) and item >= 0 for item in value):
                raise ValidationError('Flags must be a list of non-negative integers')
        return value

    def validate_groups(self, value):
        """
        Validate the "groups" field.
        """
        if value is not None:
            if not isinstance(value, list):
                raise ValidationError('Flags must be a list of integers')
            if not all(isinstance(item, int) and item >= 0 for item in value):
                raise ValidationError('Flags must be a list of non-negative integers')
        return value

    def validate_expertise(self, value):
        """
        Validate the "expertise" field.
        """
        if value is not None:
            if not isinstance(value, list):
                raise ValidationError('Flags must be a list of integers')
            if not all(isinstance(item, int) and item >= 0 for item in value):
                raise ValidationError('Flags must be a list of non-negative integers')
        return value

    def validate_sort_direction(self, value):
        """
        Validate the "sort_direction" field.
        """
        if value.lower() not in ['asc', 'desc']:
            raise ValidationError('Invalid value for sort_direction. It must be "asc" or "desc".')
        return value

    def validate_page(self, value):
        """
        Validate the "page" field.
        """
        if value < 0:
            raise ValidationError('Page number must be a non-negative integer')
        return value

    def validate_page_size(self, value):
        """
        Validate the "page_size" field.
        """
        if value < 8 or value > 120:
            raise ValidationError('Page size must be between 8 and 120')
        return value

    def to_internal_value(self, data):
        """
        Convert the "sex" and "age_direction" value to lowercase before validation
        ("m" or "f", "below" or "above", respectively)
        """
        if 'sex' in data and data['sex'] is not None:
            data['sex'] = data['sex'].lower()
        return super().to_internal_value(data)


# noinspection PyMethodMayBeStatic
class TheoryRequestSerializer(CommonRequestSerializer):
    allowed_fields = ['id', 'title', 'type', 'publish_date']

    type = serializers.CharField(required=True)
    sort_by = serializers.ChoiceField(choices=allowed_fields, required=False, default='id')
    sort_direction = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')
    date_min = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    date_max = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    filter = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=100)

    def validate(self, data):
        """
        Custom validation for date_min and date_max
        """
        date_min = data.get('date_min')
        date_max = data.get('date_max')
        if date_min and date_max:
            try:
                date_min = datetime.strptime(date_min, '%d.%m.%Y')
                date_max = datetime.strptime(date_max, '%d.%m.%Y')
            except ValueError:
                raise ValidationError('Invalid date format. Use DD.MM.YYYY format')
            if date_min > date_max:
                raise ValidationError('date_min should be less than or equal to date_max')
        return data

    def validate_type(self, value):
        """
        Validate the "type" field
        """
        if value.lower() != 'general':
            raise ValidationError('Invalid request type, "general" expected')
        return value

    def validate_filter(self, value):
        """
        Validate the "filter" value to match wildcard mask
        """
        if value is None or value.strip() == '':
            return value

        valid_wildcard_mask = re.compile(r'^[\w\s*?]+$')

        if not valid_wildcard_mask.match(value):
            raise ValidationError('Invalid filter format: it must be a valid wildcard mask or empty')

        return value

    def to_internal_value(self, data):
        """
        Convert the "type" value to lowercase before validation
        """
        if 'type' in data and data['type'] is not None:
            data['type'] = data['type'].lower()
        return super().to_internal_value(data)


class OrgsRequestSerializer(CommonRequestSerializer):
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

    allowed_fields = ['id', 'name', 'short_name']
    type = serializers.CharField(required=True)
    page = serializers.IntegerField(required=True, min_value=0)
    page_size = serializers.IntegerField(required=True, min_value=8, max_value=120)
    sort_by = serializers.ChoiceField(choices=allowed_fields, required=False, default='id')
    sort_direction = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')
    filter = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=100)


    def validate_type(self, value):
        """
        Validate the "type" field
        """
        if value.lower() != 'page':
            raise ValidationError('Invalid request type, "page" expected')
        return value

    def validate_filter(self, value):
        """
        Validate the "filter" value to match wildcard mask
        """
        if value is None or value.strip() == '':
            return value

        valid_wildcard_mask = re.compile(r'^[\w\s*?]+$')

        if not valid_wildcard_mask.match(value):
            raise ValidationError('Invalid filter format: it must be a valid wildcard mask or empty')

        return value

    def validate_sort_direction(self, value):
        """
        Validate the "sort_direction" field.
        """
        if value.lower() not in ['asc', 'desc']:
            raise ValidationError('Invalid value for sort_direction. It must be "asc" or "desc".')
        return value

    def validate_page(self, value):
        """
        Validate the "page" field.
        """
        if value < 0:
            raise ValidationError('Page number must be a non-negative integer')
        return value

    def validate_page_size(self, value):
        """
        Validate the "page_size" field.
        """
        if value < 8 or value > 120:
            raise ValidationError('Page size must be between 8 and 120')
        return value

    def to_internal_value(self, data):
        """
        Convert the "sex" and "age_direction" value to lowercase before validation
        ("m" or "f", "below" or "above", respectively)
        """
        if 'sex' in data and data['sex'] is not None:
            data['sex'] = data['sex'].lower()
        return super().to_internal_value(data)