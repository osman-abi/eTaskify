import factory
from factory.django import DjangoModelFactory

from apps.tasks.models import Task

from tests.test_company.factories import CompanyFactory
from tests.test_users.factories import UserFactory


class TaskFactory(DjangoModelFactory):
    """
    Factory for creating Task instances.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    class Meta:
        model = Task

    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('text')
    status = factory.Faker('random_element', elements=[choice[0] for choice in STATUS_CHOICES])
    assignee = factory.SubFactory(UserFactory)
    company = factory.SubFactory(CompanyFactory)
    created_by = factory.SubFactory(UserFactory)
    deadline = factory.Faker('future_datetime', end_date='+30d', tzinfo=None)


    # @factory.post_generation
    # def assignee(self, create, extracted, **kwargs):
    #     """
    #     Assign users to the task.
    #     """
    #     if not create:
    #         return
    #
    #     if extracted:
    #         for user in extracted:
    #             self.assignee.set(user)