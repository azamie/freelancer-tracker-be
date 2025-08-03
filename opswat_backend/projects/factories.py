import factory
from factory import fuzzy
from faker import Faker

from opswat_backend.users.factories import UserFactory

from .models import Project

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
