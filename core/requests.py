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
    """
    Filters:
    * Alive: If the value `alive: true` or `alive: false` is defined, we perform the respective query.
      In other words, if we define `alive: true`, we return only alive people, if `alive: false`,
      we return only dead people, if we don't define `alive`, we return everyone.
    * Traitor to Ukraine: If the value `is_ttu: true` or `is_ttu: false` is defined, we perform the respective query.
      If undefined, we return everyone
    * Foreign Friend: If the value `is_ff: true` or `is_ff: false` is defined, we perform the respective query.
      If undefined, we return everyone
    * Sex (gender): If the value `sex: "M"` or `sex: "F"` is defined, we perform the respective query.
      If undefined, we return both men and women
    * Full name: If the filter value in wildcard format is defined, we perform the respective query.
      E.g. `"filter": "Ivan*"` will return all people whose full name starts with "Ivan"
      If undefined, we return everyone
    * Age: If the value `age: N` is defined, we perform the respective query.
      Age direction Should be also defined: `age_direction: "below"` or `age_direction: "above"`
      Default direction is "below"
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

    allowed_fields = ['id', 'fullname_en', 'fullname_ru', 'fullname_uk', 'dob', 'dod', 'sex']
    type = serializers.CharField(required=True)
    page = serializers.IntegerField(required=True, min_value=0)
    page_size = serializers.IntegerField(required=True, min_value=8, max_value=120)
    sort_by = serializers.ChoiceField(choices=allowed_fields, required=False, default='id')
    sort_direction = serializers.ChoiceField(choices=['asc', 'desc'], required=False, default='asc')
    filter = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=100)
    alive = serializers.BooleanField(required=False, allow_null=True)
    sex = serializers.ChoiceField(choices=[('m', 'm'), ('f', 'f')], required=False)
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
        """
        Convert a parameter to tristate value (True, False, None)
        """
        return self.tristate_param(value)

    def validate_is_ttu(self, value):
        """
        Convert a parameter to tristate value (True, False, None)
        """
        return self.tristate_param(value)

    def validate_is_ff(self, value):
        """
        Convert a parameter to tristate value (True, False, None)
        """
        return self.tristate_param(value)

    def to_internal_value(self, data):
        """
        Convert the "sex" and "age_direction" value to lowercase before validation
        ("m" or "f", "below" or "above", respectively)
        """
        if 'sex' in data:
            data['sex'] = data['sex'].lower()
        if 'age_direction' in data:
            data['age_direction'] = data['age_direction'].lower()
        return super().to_internal_value(data)
