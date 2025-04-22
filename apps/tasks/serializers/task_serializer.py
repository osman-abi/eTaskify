from rest_framework import serializers

from ..models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    """

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
