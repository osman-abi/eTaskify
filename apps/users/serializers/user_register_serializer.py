from rest_framework import serializers
from django.core.validators import EmailValidator

from ..models import BaseUser


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = BaseUser
        fields = ('email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        """
        Create a new admin user with the provided validated data. Because in the first registration admin user will be
        created to create Organization Company and the other STAFF users. So we are using create_superuser method.
        STAFF user can only log in to our app. NOT registration.
        """
        user = BaseUser.objects.create_superuser(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
        )
        return user

    def validate_email(self, value):
        """
        Validate the email address.
        """
        if not value:
            raise serializers.ValidationError("This field may not be blank.")
        if BaseUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        try:
            EmailValidator()(value)
        except serializers.ValidationError:
            raise serializers.ValidationError("Invalid email format.")

        return value

    def validate_password(self, value):
        """
        Validate the password.
        """
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        if not value:
            raise serializers.ValidationError("This field may not be blank.")

        return value

    def validate_first_name(self, value):
        """
        Validate the first name.
        """
        if not value:
            raise serializers.ValidationError("First name may not be blank.")
        return value

    def validate_last_name(self, value):
        """
        Validate the last name.
        """
        if not value:
            raise serializers.ValidationError("Last name may not be blank.")
        return value
