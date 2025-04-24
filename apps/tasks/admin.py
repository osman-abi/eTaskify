from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the Task model.
    """
    list_display = ('title', 'description', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('title', 'description')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )