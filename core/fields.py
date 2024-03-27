from abc import ABC
from rest_framework import serializers


class UnixTimestampField(serializers.Field, ABC):
    """
    Serializer field to convert datetime to Unix timestamp
    """

    def to_representation(self, value):
        """
        Convert the datetime to Unix timestamp for serialization
        """
        if value:
            return int(value.timestamp())
        return None
