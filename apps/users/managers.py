import random
import string

from django.contrib.auth.models import BaseUserManager

from utils import EmailData


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
        extra_fields.setdefault('is_active', True)
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=13))

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff user must have is_staff=True.')
        if extra_fields.get('is_admin') is not False:
            raise ValueError('Staff user must have is_admin=False.')

        user = self.create_user(email, password, **extra_fields)
        # # Send email to user with the password
        self._send_email_to_staff(user.email, password, fullname=user.get_full_name(), company_name=user.company.name)
        return user

    def _send_email_to_staff(self, staff_email: str, password: str, fullname: str, company_name: str) -> None:
        """
        Send an email to the staff user.
        """
        email_data = EmailData(email_to=[staff_email], fullname=fullname, company_name=company_name, password=password)
        email_data.send_create_staff_email()
