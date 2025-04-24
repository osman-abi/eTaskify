import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestCompanyView:

    def test_create_company(self, client, admin_user, company_data):
        """
        Test creating a company.
        """
        client.force_authenticate(user=admin_user)
        response = client.post(reverse("company-list"), data=company_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == company_data["name"]
        assert response.data["address"] == company_data["address"]
        assert response.data["phone_number"] == company_data["phone_number"]

    def test_create_company_invalid_data(self, client, admin_user, company_data):
        """
        Test creating a company with invalid data.
        """
        client.force_authenticate(user=admin_user)
        company_data["name"] = ""
        response = client.post(reverse("company-list"), data=company_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "This field may not be blank." in response.data["name"]

    def test_create_company_unauthenticated(self, client, company_data):
        """
        Test creating a company without authentication.
        """
        response = client.post(reverse("company-list"), data=company_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        'field, value, expected_error',
        [
            ("name", "", "This field may not be blank.")
        ],
    )
    def test_create_company_missing_fields(self, client, admin_user, company_data, field, value, expected_error):
        """
        Test creating a company with invalid data.
        """
        client.force_authenticate(user=admin_user)
        company_data[field] = value
        response = client.post(reverse("company-list"), data=company_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[field][0] == expected_error

    def test_create_company_non_admin_invalid_permissions(self, client, staff_user, company_data):
        """
        Test creating a company with a non-admin user.
        """
        client.force_authenticate(user=staff_user)
        response = client.post(reverse("company-list"), data=company_data)
        print("response", response.data, response.status_code)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[0] == "User is not admin role."

    def test_get_tasks_for_company(self, client, staff_user, company, task_list):
        """
        Test retrieving tasks for a specific company.
        """
        client.force_authenticate(user=staff_user)
        url = reverse("company-tasks", args=[company.id])
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_get_tasks_for_company_unauthenticated(self, client, company):
        """
        Test retrieving tasks for a specific company without authentication.
        """
        url = reverse("company-tasks", args=[company.id])
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "Authentication credentials were not provided."
