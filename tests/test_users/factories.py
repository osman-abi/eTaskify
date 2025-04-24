from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from apps.users.models import BaseUser


class UserFactory(DjangoModelFactory):
    """
    Factory for creating BaseUser instances.
    """

    class Meta:
        model = BaseUser
        django_get_or_create = ('email',)

    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    password = Faker('password')
    company = SubFactory('tests.test_company.factories.CompanyFactory')
    is_active = True
    is_staff = False
    is_superuser = False
    is_admin = False
