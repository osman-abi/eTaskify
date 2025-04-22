from rest_framework import serializers

from apps.users.models import BaseUser
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

    def update(self, instance, validated_data):
        """
        Update the task instance with the new assignee.
        """
        assignee_ids = validated_data.get('assignee', [])
        users = BaseUser.objects.filter(id__in=assignee_ids)
        instance.assignee.set(users)
        instance.save()
        return instance
