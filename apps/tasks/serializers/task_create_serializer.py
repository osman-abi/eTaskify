from django.utils import timezone
from rest_framework import serializers

from apps.users.models import BaseUser
from ..models import Task


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a Task.
    """

    assignee = serializers.ListSerializer(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text="List of user IDs to assign to the task",
    )

    class Meta:
        model = Task
        fields = ["title", "description", "deadline", "assignee", "status"]
        read_only_fields = ["created_by", "created_at", "updated_at", "status"]

    def create(self, validated_data):
        """
        Create and return a new Task instance, including the assignee.
        """
        assignee_ids = validated_data.pop("assignee", [])
        company = self.context["request"].user.company
        created_by = self.context["request"].user
        task = Task.objects.create(
            company=company, created_by=created_by, **validated_data
        )
        user = self.context["request"].user
        task.created_by = user
        task.save()
        if assignee_ids:
            users = BaseUser.objects.filter(id__in=assignee_ids)
            task.assignee.set(users)
        return task

    def validate_deadline(self, value):
        """
        Validate that the deadline is not in the past.
        """
        if value < timezone.now():
            raise serializers.ValidationError("Deadline cannot be in the past.")
        return value
