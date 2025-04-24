import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUserLogOut:

    def test_user_logout(self, client, staff_user, refresh_token):
        """
        Test user logout endpoint.
        """
        url = reverse('user-logout')
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh_token.access_token)}')
        response = client.post(url, data={"refresh_token": refresh_token})

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert 'access' not in response.data
        assert 'refresh' not in response.data

    def test_user_logout_with_invalid_token(self, client, staff_user):
        """
        Test user logout endpoint with invalid token.
        """
        url = reverse('user-logout')
        client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        response = client.post(url, data={"refresh_token": "invalid_token"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_logout_without_refresh(self, client, staff_user, refresh_token):
        """
        Test user logout endpoint with empty token.
        """
        url = reverse('user-logout')
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh_token.access_token)}')
        response = client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['refresh_token'][0] == 'This field is required.'

    def test_user_logout_with_expired_token(self, client, staff_user, refresh_token, expired_refresh_token):
        """
        Test user logout endpoint with expired token.
        """
        url = reverse('user-logout')
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh_token.access_token)}')
        response = client.post(url, data={"refresh_token": expired_refresh_token})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[0] == 'Token is invalid or expired.'
