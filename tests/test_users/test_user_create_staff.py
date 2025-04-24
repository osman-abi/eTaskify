import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUserCreateStaff:

    def test_user_create_staff(self, client, admin_user, user_data):
        url = reverse('user-staff')
        client.force_authenticate(user=admin_user)
        response = client.post(url, data=user_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_user_create_unauthenticated(self, client, user_data):
        url = reverse('user-staff')
        response = client.post(url, data=user_data)
        print(response.data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data['detail'] == 'Authentication credentials were not provided.'

    def test_user_create_staff_not_admin(self, client, staff_user, user_data):
        url = reverse('user-staff')
        client.force_authenticate(user=staff_user)
        response = client.post(url, data=user_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data['detail'] == 'You do not have permission to perform this action.'

    def test_user_create_staff_email_exist(self, client, admin_user, staff_user, user_data):
        url = reverse('user-staff')
        client.force_authenticate(user=admin_user)
        user_data['email'] = staff_user.email
        response = client.post(url, data=user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'][0] == 'Email already exists.'
