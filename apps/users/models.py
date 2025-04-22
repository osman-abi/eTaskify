import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from apps.company.models import Company


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and returns a user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    def create_staff_user(self, email, **extra_fields):
        """
        Creates and returns a staff user with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', False)

        password = random.choice(string.ascii_letters) + str(random.randint(1000, 9999))

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff user must have is_staff=True.')
        if extra_fields.get('is_admin') is not False:
            raise ValueError('Staff user must have is_admin=False.')

        # user = self.create_user(email, password, **extra_fields)
        # # Send email to user with the password
        # # send_email(user.email, password)
        return self.create_user(email, password, **extra_fields)


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
