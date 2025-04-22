from django.db import models

from apps.users.models import BaseUser


class Task(models.Model):
    """
    Model representing a task.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    assignee = models.ManyToManyField(BaseUser, related_name='tasks', blank=True,
                                      help_text="Users assigned to this task")
    created_by = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='created_tasks',
                                   help_text="User who created this task")
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
