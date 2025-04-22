from django.contrib import auth
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import BaseUser


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user login.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = BaseUser
        fields = ("email", "password")

    def validate(self, attrs):
        """
        Validate the user credentials.
        """
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        filtered_user_by_email = BaseUser.objects.filter(email=email)
        if filtered_user_by_email is None:
            raise serializers.ValidationError("User with this email does not exist.")

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials, try again")

        token = RefreshToken.for_user(user)
        attrs["refresh"] = str(token)
        attrs["access"] = str(token.access_token)

        return attrs
