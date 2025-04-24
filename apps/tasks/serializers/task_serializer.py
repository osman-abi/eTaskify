from rest_framework import serializers

from apps.users.serializers import UserListSerializer
from ..models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    """

    created_by = UserListSerializer(read_only=True)
    assignee = UserListSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "deadline",
            "created_by",
            "assignee",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("created_at", "updated_at")
