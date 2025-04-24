import pytest
from .factories import UserFactory


@pytest.fixture
def admin_user():
    """
    Fixture for creating a user instance.
    """
    return UserFactory(is_superuser=True, is_staff=True)


@pytest.fixture
def staff_user():
    """
    Fixture for creating a staff user instance.
    """
    return UserFactory(is_superuser=False, is_admin=False, is_staff=True)


@pytest.fixture
def user_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "testemail@gmail.com",
        "password": "password123",
    }