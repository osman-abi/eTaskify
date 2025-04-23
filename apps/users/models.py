from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.company.models import Company
from .managers import CustomUserManager


class BaseUser(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(
        max_length=128,
        help_text='Password must be at least 6 characters long and contain at least one letter and one number.'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='users',
        help_text='Company associated with the user.'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class StaffUser(BaseUser):
    """
    Staff user model.
    """

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Staff User'
        verbose_name_plural = 'Staff Users'
