import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUserLogIn:
    """
    Test suite for user login.
    """

    def test_user_login(self, client, staff_user):
        """
        Test user login endpoint.
        """
        url = reverse('user_login')
        user_data = {
            "email": staff_user.email,
            "password": "password123",
        }
        response = client.post(url, data=user_data)
        print(response.data)

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_user_login_with_invalid_credentials(self, client, staff_user):
        """
        Test user login endpoint with invalid credentials.
        """
        url = reverse('user_login')
        user_data = {
            "email": staff_user.email,
            "password": "wrongpassword",
        }
        response = client.post(url, data=user_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'access' not in response.data
        assert 'refresh' not in response.data
