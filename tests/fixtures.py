import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    """
    Fixture for creating an API client instance.
    """
    return APIClient()
