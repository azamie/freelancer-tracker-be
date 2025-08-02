from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import EmailField
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    first_name = CharField(_("first name"), max_length=150)
    last_name = CharField(_("last name"), max_length=150)
    email = EmailField(_("email address"), unique=True)

    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()
