import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUserRegister:
    """
    Test suite for user registration.
    """

    def test_user_registration(self, client, user_data):
        """
        Test user registration endpoint.
        """
        url = reverse('user-register')
        response = client.post(url, data=user_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] == user_data['email']

    def test_register_with_invalid_email(self, client, user_data):
        """
        Test registration with an invalid email format.
        """
        user_data['email'] = 'invalid-email'
        url = reverse('user-register')
        response = client.post(url, data=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data
        assert response.data['email'][0] == 'Enter a valid email address.'

    def test_register_with_existing_email(self, client, user_data, admin_user):
        """
        Test registration with an already existing email.
        """
        admin_user.email = user_data['email']
        admin_user.save()
        url = reverse('user-register')
        response = client.post(url, data=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data
        assert response.data['email'][0] == 'Email already exists.'

    @pytest.mark.parametrize(
        'field, value, expected_error',
        [
            ('password', 'short', 'Password must be at least 6 characters long.'),
            ('password', 'testtest', 'Password must contain at least one number.'),
            ('password', '123456789', 'Password must contain at least one letter.'),
        ]
    )
    def test_register_with_invalid_password(self, client, user_data, field, value, expected_error):
        """
        Test registration with an invalid password format.
        """
        user_data['password'] = value
        url = reverse('user-register')
        response = client.post(url, data=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field in response.data
        assert response.data[field][0] == expected_error

    @pytest.mark.parametrize(
        'field, value, expected_error',
        [
            ('first_name', '', 'First name may not be blank.'),
            ('last_name', '', 'Last name may not be blank.'),
            ('email', '', 'This field may not be blank.'),
            ('password', '', 'This field may not be blank.'),
        ]
    )
    def test_register_with_missing_fields(self, client, user_data, field, value, expected_error):
        """
        Test registration with missing required fields.
        """
        user_data[field] = value
        url = reverse('user-register')
        response = client.post(url, data=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field in response.data
        assert response.data[field][0] == expected_error
