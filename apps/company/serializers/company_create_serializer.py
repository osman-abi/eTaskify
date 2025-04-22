from rest_framework import serializers

from apps.users.models import BaseUser
from ..models import Company


class CompanyCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new company.
    """

    class Meta:
        model = Company
        fields = ('name', 'address', 'phone_number')

    def create(self, validated_data):
        """
        Create a new company with the provided validated data.
        """
        user = self.context['request'].user
        if not user.is_authenticated:
            raise serializers.ValidationError("User is not authenticated.")
        if not user.is_admin:
            raise serializers.ValidationError("User is not admin role.")
        user = BaseUser.objects.get(email=user.email)
        company = Company.objects.create(**validated_data)
        company.users.add(user)
        return company
