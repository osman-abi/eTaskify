from ..models import BaseUser
from rest_framework import serializers

class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = BaseUser
        fields = ('email', 'password')

    def validate(self, attrs):
        """
        Validate the user credentials.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        user = BaseUser.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        return attrs

    def save(self, **kwargs):
        """
        Save the user instance.
        """
        user = BaseUser.objects.get(email=self.validated_data['email'])
        return user