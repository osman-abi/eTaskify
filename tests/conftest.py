from datetime import timedelta

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from tests.test_company.factories import CompanyFactory
from tests.test_tasks.factories import TaskFactory
from tests.test_users.factories import UserFactory


@pytest.fixture
def admin_user(db):
    """
    Fixture for creating a user instance.
    """
    user = UserFactory(is_admin=True)
    user.set_password("password123")
    user.save()
    return user


@pytest.fixture
def staff_user(db):
    user = UserFactory(is_staff=True)
    user.set_password("password123")
    user.save()
    return user


@pytest.fixture
def user_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "testemail@gmail.com",
        "password": "password123",
    }


@pytest.fixture
def company_data():
    return {
        "name": "Test Company",
        "address": "123 Test St",
        "phone_number": "+1234567890",
    }


@pytest.fixture
def company():
    """
    Fixture for creating a company instance.
    """
    return CompanyFactory()


@pytest.fixture
def task(company):
    """
    Fixture for creating a task instance.
    """
    return TaskFactory()


@pytest.fixture
def refresh_token(staff_user):
    """
    Fixture for creating a JWT token for the admin user.
    """
    refresh = RefreshToken.for_user(staff_user)
    return refresh


@pytest.fixture
def expired_refresh_token(staff_user):
    """
    Fixture for creating an expired JWT token for the admin user.
    """
    refresh = RefreshToken.for_user(staff_user)
    refresh.set_exp(lifetime=timedelta(days=-1))
    return refresh


@pytest.fixture
def user_list():
    """
    Fixture for creating a list of user instances.
    """
    return UserFactory.create_batch(10)


@pytest.fixture
def task_list():
    """
    Fixture for creating a list of task instances.
    """
    return TaskFactory.create_batch(10)


@pytest.fixture
def client():
    """
    Fixture for creating an API client instance.
    """
    return APIClient()
