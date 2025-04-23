from rest_framework import serializers

from apps.users.models import BaseUser
from utils import EmailData
from ..models import Task


class TaskAssignSerializer(serializers.ModelSerializer):
    """
    Serializer for assigning users to a task.
    """

    assignee = serializers.ListSerializer(
        child=serializers.IntegerField(),
        write_only=True,
        help_text="List of user IDs to assign to the task"
    )

    class Meta:
        model = Task
        fields = ['assignee']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def validate_assignee(self, value):
        """
        Validate the list of assignee IDs.
        """
        if not isinstance(value, list):
            raise serializers.ValidationError("Assignee must be a list of user IDs.")
        if len(value) == 0:
            raise serializers.ValidationError("Assignee list cannot be empty.")
        return value

    def update(self, instance, validated_data):
        """
        Update the task instance with the new assignee.
        """
        assignee_ids = validated_data.get('assignee', [])
        users = BaseUser.objects.filter(id__in=assignee_ids)
        instance.assignee.set(users)
        instance.save()
        assignee_emails = list(users.values_list('email', flat=True))
        self._send_email_to_assignee(assignee_emails, instance.id, instance.title)
        return instance

    def _send_email_to_assignee(self, assignee: list, task_id: int, task_title: str) -> None:
        """
        Send an email to the assignee.
        """
        # Implement email sending logic here
        if not assignee:
            raise ValueError("Assignee list cannot be empty.")
        email_data = EmailData(email_to=assignee, task_id=task_id, task_title=task_title)
        email_data.send_task_assigned_email()
