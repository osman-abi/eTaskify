import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestTask:

    def test_create_task(self, client, staff_user, task, company):
        """
        Test creating a task.
        """
        task.company = company
        # task.assignee = staff_user
        # task.created_by = staff_user
        task.save()
        client.force_authenticate(user=staff_user)
        url = reverse("task-list")
        response = client.post(
            url,
            data={
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "assignee": [staff_user.id],
                "deadline": task.deadline,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == task.title
        assert response.data["description"] == task.description
        assert response.data["status"] == 'pending'
        assert response.data["deadline"] == task.deadline.isoformat().replace('+00:00', 'Z')

    def test_create_task_unauthenticated(self, client, staff_user, task, company):
        """
        Test creating a task without authentication.
        """
        url = reverse("task-list")
        response = client.post(
            url,
            data={
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "assignee": [staff_user.id],
                "deadline": task.deadline,
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "Authentication credentials were not provided."

    def test_assign_task(self, client, staff_user, task):
        """
        Test assigning a task to a user.
        """
        client.force_authenticate(user=staff_user)
        url = reverse("task-assign", args=[task.id])
        data = {
            "assignee": [staff_user.id]
        }

        response = client.put(
            url,
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["assignee"][0] == staff_user.email

    def test_assign_task_unauthenticated(self, client, task):
        """
        Test assigning a task without authentication.
        """
        url = reverse("task-assign", args=[task.id])
        data = {
            "assignee": [1]
        }
        response = client.put(
            url,
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "Authentication credentials were not provided."

    def test_update_task(self, client, staff_user, task):
        """
        Test updating a task.
        """
        client.force_authenticate(user=staff_user)
        url = reverse("task-detail", args=[task.id])
        data = {
            "title": "Updated Task Title",
            "description": "Updated description",
            "status": "completed",
            "deadline": task.deadline,
        }
        response = client.patch(
            url,
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == data["title"]
        assert response.data["description"] == data["description"]
        assert response.data["status"] == data["status"]
        assert response.data["deadline"] == task.deadline.isoformat().replace('+00:00', 'Z')

    def test_update_task_unauthenticated(self, client, task):
        """
        Test updating a task without authentication.
        """
        url = reverse("task-detail", args=[task.id])
        data = {
            "title": "Updated Task Title",
            "description": "Updated description",
            "status": "completed",
            "deadline": task.deadline,
        }
        response = client.patch(
            url,
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "Authentication credentials were not provided."

    def test_delete_task(self, client, staff_user, task):
        """
        Test deleting a task.
        """
        client.force_authenticate(user=staff_user)
        url = reverse("task-detail", args=[task.id])
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_task_unauthenticated(self, client, task):
        """
        Test deleting a task without authentication.
        """
        url = reverse("task-detail", args=[task.id])
        response = client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "Authentication credentials were not provided."
