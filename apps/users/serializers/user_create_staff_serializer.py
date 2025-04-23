from rest_framework import serializers

from ..models import BaseUser


class UserCreateStaffSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a staff user.
    """
    email = serializers.EmailField(required=True)

    class Meta:
        model = BaseUser
        fields = ('email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, attrs):
        """
        Validate the input data.
        """
        email = attrs.get('email')
        if not email:
            raise serializers.ValidationError("Email is required.")
        if BaseUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")
        if not attrs.get('first_name'):
            raise serializers.ValidationError("First name is required.")
        if not attrs.get('last_name'):
            raise serializers.ValidationError("Last name is required.")
        return attrs

    def create(self, validated_data):
        """
        Create a new staff user with the provided validated data. Staff user can only log in to our app. NOT registration.
        """
        user = BaseUser.objects.create_staff_user(
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
        )
        request_user = self.context['request'].user
        if not request_user.is_authenticated:
            raise serializers.ValidationError("User is not authenticated.")
        if not request_user.is_admin:
            raise serializers.ValidationError("User is not admin role.")
        user.company = request_user.company
        user.save()
        return user
