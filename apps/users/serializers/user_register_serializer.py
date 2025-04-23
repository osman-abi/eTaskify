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
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

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
        if not attrs.get('password'):
            raise serializers.ValidationError("Password is required.")
        if len(attrs.get('password')) < 6 and \
                not any(char.isalpha() for char in attrs.get('password')) and \
                not any(char.isdigit() for char in attrs.get('password')):
            raise serializers.ValidationError(
                "Password must be at least 6 characters long and contain at least one letter and one number.")

        return attrs
