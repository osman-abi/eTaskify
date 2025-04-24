from django.utils import timezone
from rest_framework import serializers

from ..models import Task


class TaskUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a Task.
    """
    status = serializers.ChoiceField(
        choices=["pending", "in_progress", "completed"],
        required=False,
        allow_blank=False,
    )

    class Meta:
        model = Task
        fields = ["title", "description", "status", "deadline"]
        read_only_fields = ["created_by", "created_at", "updated_at"]
        extra_kwargs = {
            "title": {"required": False},
            "description": {"required": False},
            "status": {"required": False},
            "deadline": {"required": False},
        }

    def validate_deadline(self, value):
        """
        Validate that the deadline is not in the past.
        """
        if value < timezone.now():
            raise serializers.ValidationError("Deadline cannot be in the past.")
        return value

    def validate_status(self, value):
        """
        Validate that the status is one of the allowed values.
        """
        allowed_statuses = ["pending", "in_progress", "completed"]
        if value not in allowed_statuses:
            raise serializers.ValidationError(f"Status must be one of {allowed_statuses}.")
        return value

    def update(self, instance, validated_data):
        """
        Update and return an existing Task instance.
        """
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.status = validated_data.get("status", instance.status)
        instance.deadline = validated_data.get("deadline", instance.deadline)
        instance.save()
        return instance
