import factory
from factory import fuzzy
from faker import Faker
from projects.factories import ProjectFactory

from .models import GitHubActivity
from .models import Repository

fake = Faker()


class RepositoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Repository

    project = factory.SubFactory(ProjectFactory)
    repo_name = factory.Faker("slug")
    url = factory.LazyAttribute(
        lambda obj: f"https://github.com/{fake.user_name()}/{obj.repo_name}",
    )


class GitHubActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GitHubActivity

    repository = factory.SubFactory(RepositoryFactory)
    activity_type = fuzzy.FuzzyChoice(
        [choice[0] for choice in GitHubActivity.ActivityType.choices],
    )
    username = factory.Faker("user_name")
    details = factory.LazyAttribute(lambda obj: _generate_details(obj.activity_type))


def _generate_details(activity_type):
    if activity_type == GitHubActivity.ActivityType.PUSH_COMMITS:
        commit_count = fake.random_int(min=1, max=5)
        return {
            "commits": [
                {
                    "sha": fake.sha1(),
                    "message": fake.sentence(nb_words=6),
                    "author": fake.user_name(),
                    "timestamp": fake.iso8601(),
                }
                for _ in range(commit_count)
            ],
            "source_branch": f"feature/{fake.slug()}",
            "target_branch": "main",
        }

    if activity_type == GitHubActivity.ActivityType.CREATE_PR:
        return {
            "pr_number": fake.random_int(min=1, max=999),
            "title": fake.sentence(nb_words=8),
            "source_branch": f"feature/{fake.slug()}",
            "target_branch": "main",
            "description": fake.text(max_nb_chars=300),
        }

    if activity_type == GitHubActivity.ActivityType.MERGE_PR:
        return {
            "pr_number": fake.random_int(min=1, max=999),
            "title": fake.sentence(nb_words=8),
            "source_branch": f"feature/{fake.slug()}",
            "target_branch": "main",
            "merge_commit_sha": fake.sha1(),
        }

    if activity_type == GitHubActivity.ActivityType.CREATE_RELEASE:
        return {
            "tag_name": (
                f"v{fake.random_int(min=1, max=9)}."
                f"{fake.random_int(min=0, max=9)}."
                f"{fake.random_int(min=0, max=9)}"
            ),
            "release_name": fake.catch_phrase(),
            "description": fake.text(max_nb_chars=200),
            "target_branch": "main",
        }

    return {}
