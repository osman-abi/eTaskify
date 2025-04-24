import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from apps.tasks.models import Task
from tests.test_company.factories import CompanyFactory
from tests.test_users.factories import UserFactory

STATUS_CHOICES = [
    ("pending", "Pending"),
    ("in_progress", "In Progress"),
    ("completed", "Completed"),
]


class TaskFactory(DjangoModelFactory):
    """
    Factory for creating Task instances.
    """

    class Meta:
        model = Task
        skip_postgeneration_save = True

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("text")
    status = factory.Faker(
        "random_element", elements=[choice[0] for choice in STATUS_CHOICES]
    )
    company = factory.SubFactory(CompanyFactory)
    created_by = factory.SubFactory(UserFactory)
    deadline = factory.LazyFunction(
        lambda: timezone.make_aware(
            factory.Faker("future_datetime", end_date="+30d").evaluate(
                None, None, {"locale": None}
            )
        )
    )

    @factory.post_generation
    def assignee(self, create, extracted, **kwargs):
        """
        Assign users to the task.
        """
        if not create:
            return

        if extracted:
            for user in extracted:
                self.assignee.set(user)
