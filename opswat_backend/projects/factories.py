import factory
from factory import fuzzy
from faker import Faker

from opswat_backend.users.factories import UserFactory

from .models import Invoice
from .models import Project
from .models import Task

fake = Faker()


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Faker("catch_phrase")
    description = factory.Faker("text", max_nb_chars=500)
    status = fuzzy.FuzzyChoice([choice[0] for choice in Project.Status.choices])
    user = factory.SubFactory(UserFactory)
    start_date = factory.Faker("date_time_this_year", tzinfo=None)
    end_date = factory.LazyAttribute(
        lambda obj: fake.date_time_between(start_date=obj.start_date, end_date="+1y")
        if obj.start_date
        else None,
    )


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    name = factory.Faker("sentence", nb_words=3)
    task_type = fuzzy.FuzzyChoice([choice[0] for choice in Task.TaskType.choices])
    status = fuzzy.FuzzyChoice([choice[0] for choice in Task.Status.choices])
    description = factory.Faker("text", max_nb_chars=300)
    project = factory.SubFactory(ProjectFactory)


class InvoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Invoice

    amount = fuzzy.FuzzyDecimal(100.00, 5000.00, precision=2)
    status = fuzzy.FuzzyChoice([choice[0] for choice in Invoice.Status.choices])
    due_date = factory.Faker("future_datetime", end_date="+30d", tzinfo=None)
    project = factory.SubFactory(ProjectFactory)
