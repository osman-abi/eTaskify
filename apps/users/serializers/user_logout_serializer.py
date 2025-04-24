from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserLogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout.
    """

    refresh_token = serializers.CharField()

    def validate_refresh_token(self, value):
        """
        Validate the refresh token.
        """
        if not value:
            raise serializers.ValidationError("This field is required.")
        return value

    def save(self, **kwargs):
        """
        Save the serializer data.
        """
        refresh_token = self.validated_data.get("refresh_token")
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            raise serializers.ValidationError("Token is invalid or expired.")
