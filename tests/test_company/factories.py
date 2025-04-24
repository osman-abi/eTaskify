from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from apps.company.models import Company


class CompanyFactory(DjangoModelFactory):
    """
    Factory for creating Company instances.
    """

    class Meta:
        model = Company
        django_get_or_create = ('name',)

    name = Faker('company')
    address = Faker('address')
    phone_number = Faker('phone_number')
