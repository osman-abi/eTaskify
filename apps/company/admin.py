from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the Company model.
    """
    list_display = ('name', 'address', 'phone_number')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'address', 'phone_number')}),
        (_('Additional Info'), {'fields': ()}),
    )