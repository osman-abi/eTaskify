from rest_framework import serializers

from ..models import BaseUser


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing users.
    """

    class Meta:
        model = BaseUser
        fields = ["id", "email", "first_name", "last_name"]
