from activities.factories import GitHubActivityFactory
from activities.factories import RepositoryFactory
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from projects.factories import InvoiceFactory
from projects.factories import ProjectFactory
from projects.factories import TaskFactory
from projects.models import Project
from projects.models import Task

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
        parser.add_argument(
            "--tasks-per-project",
            type=int,
            default=5,
            help="Number of tasks to create per project (default: 5)",
        )
        parser.add_argument(
            "--invoices-per-project",
            type=int,
            default=3,
            help="Number of invoices to create per project (default: 3)",
        )
        parser.add_argument(
            "--repositories-per-project",
            type=int,
            default=2,
            help="Number of repositories to create per project (default: 2)",
        )
        parser.add_argument(
            "--activities-per-repository",
            type=int,
            default=10,
            help="Number of GitHub activities to create per repository (default: 10)",
        )

    def _initialize_projects(self, user, num_projects):
        self.stdout.write(f"Creating {num_projects} projects for user: {user.email}")

        projects = []
        for _ in range(num_projects):
            project = ProjectFactory.create(user=user)
            projects.append(project)

        return projects

    def _initialize_tasks(self, projects, tasks_per_project):
        """Create fake tasks for the given projects."""
        total_tasks = len(projects) * tasks_per_project
        self.stdout.write(
            f"Creating {total_tasks} tasks ({tasks_per_project} per project)",
        )

        for project in projects:
            if project.status == Project.Status.UNSTARTED:
                task_status = Task.Status.UNSTARTED
            elif project.status == Project.Status.COMPLETED:
                task_status = Task.Status.ACCEPTED
            else:
                task_status = None

            for _ in range(tasks_per_project):
                if task_status:
                    TaskFactory.create(project=project, status=task_status)
                else:
                    TaskFactory.create(project=project)

    def _initialize_invoices(self, projects, invoices_per_project):
        """Create fake invoices for the given projects."""
        total_invoices = len(projects) * invoices_per_project
        self.stdout.write(
            f"Creating {total_invoices} invoices ({invoices_per_project} per project)",
        )

        for project in projects:
            for _ in range(invoices_per_project):
                InvoiceFactory.create(project=project)

    def _initialize_repositories(self, projects, repositories_per_project):
        """Create fake repositories for the given projects."""
        total_repositories = len(projects) * repositories_per_project
        self.stdout.write(
            f"Creating {total_repositories} repositories "
            f"({repositories_per_project} per project)",
        )

        repositories = []
        for project in projects:
            for _ in range(repositories_per_project):
                repository = RepositoryFactory.create(project=project)
                repositories.append(repository)

        return repositories

    def _initialize_activities(self, repositories, activities_per_repository):
        """Create fake GitHub activities for the given repositories."""
        total_activities = len(repositories) * activities_per_repository
        self.stdout.write(
            f"Creating {total_activities} GitHub activities "
            f"({activities_per_repository} per repository)",
        )

        for repository in repositories:
            for _ in range(activities_per_repository):
                GitHubActivityFactory.create(repository=repository)

    def handle(self, *args, **options):
        num_projects = options["projects"]
        tasks_per_project = options["tasks_per_project"]
        invoices_per_project = options["invoices_per_project"]
        repositories_per_project = options["repositories_per_project"]
        activities_per_repository = options["activities_per_repository"]

        self.stdout.write("Initializing fake data for the last user...")

        try:
            # Get the last user
            last_user = User.objects.last()
            if not last_user:
                self.stdout.write(
                    self.style.ERROR("No users found. Please create a user first."),
                )
                return

            projects = self._initialize_projects(last_user, num_projects)
            self._initialize_tasks(projects, tasks_per_project)
            self._initialize_invoices(projects, invoices_per_project)
            repositories = self._initialize_repositories(
                projects,
                repositories_per_project,
            )
            self._initialize_activities(repositories, activities_per_repository)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully initialize data for {last_user.email}",
                ),
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error occurred: {e}"))
