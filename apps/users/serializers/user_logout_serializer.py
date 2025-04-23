from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserLogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout.
    """

    refresh_token = serializers.CharField()

    def validate(self, attrs):
        """
        Validate the refresh token.
        """
        refresh_token = attrs.get("refresh")
        if not refresh_token:
            raise serializers.ValidationError("Refresh token is required.")

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
