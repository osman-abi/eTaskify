from django.utils import timezone
from rest_framework import serializers

from ..models import Task


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a Task.
    """

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline']

    def create(self, validated_data):
        """
        Create and return a new Task instance, including the assignee.
        """
        task = Task.objects.create(**validated_data)
        user = self.context['request'].user
        task.created_by = user
        task.save()
        return task

    def validate_deadline(self, value):
        """
        Validate that the deadline is not in the past.
        """
        if value < timezone.now():
            raise serializers.ValidationError("Deadline cannot be in the past.")
        return value
