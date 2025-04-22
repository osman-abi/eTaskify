from rest_framework import serializers

from ..models import BaseUser


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = BaseUser
        fields = ('email', 'password', 'first_name', 'last_name', 'username')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'username': {'required': False},
        }

    def create(self, validated_data):
        """
        Create a new admin user with the provided validated data. Because in the first registration admin user will be
        created to create Organization Company and the other STAFF users. So we are using create_superuser method.
        STAFF user can only log in to our app. NOT registration.
        """
        user = BaseUser.objects.create_superuser(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
        )
        return user

    def validate_email(self, value):
        """
        Validate that the email is unique.
        """
        if BaseUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        """
        Validate the password. Password should be alphanumeric and at least 6 characters long.
        """
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        if not any(char.isalpha() for char in value) or not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one letter and one number.")
        return value

    def validate_username(self, value):
        """
        Validate the username. Username should be unique.
        """
        if BaseUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value
