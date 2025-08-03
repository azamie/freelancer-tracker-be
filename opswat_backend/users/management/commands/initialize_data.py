from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from projects.factories import ProjectFactory

User = get_user_model()


class Command(BaseCommand):
    help = "Initialize fake data for development"

    def add_arguments(self, parser):
        parser.add_argument(
            "--projects",
            type=int,
            default=5,
            help="Number of projects to create (default: 5)",
        )

    def _initialize_projects(self, user, num_projects):
        """Create fake projects for the given user."""
        self.stdout.write(f"Creating {num_projects} projects for user: {user.email}")

        projects = []
        for _ in range(num_projects):
            project = ProjectFactory.create(user=user)
            projects.append(project)

        return projects

    def handle(self, *args, **options):
        num_projects = options["projects"]

        self.stdout.write("Initializing fake data for the last user...")

        try:
            # Get the last user
            last_user = User.objects.last()
            if not last_user:
                self.stdout.write(
                    self.style.ERROR("No users found. Please create a user first."),
                )
                return

            self._initialize_projects(last_user, num_projects)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully initialize data for {last_user.email}",
                ),
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error occurred: {e}"))
