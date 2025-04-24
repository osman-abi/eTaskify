import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUserList:
    """
    Test suite for user listing.
    """

    def test_user_list(self, client, admin_user, user_list):
        """
        Test user list endpoint.
        """
        client.force_authenticate(user=admin_user)
        url = reverse('user-list')
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_user_list_unauthenticated(self, client):
        """
        Test user list endpoint without authentication.
        """
        url = reverse('user-list')
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
