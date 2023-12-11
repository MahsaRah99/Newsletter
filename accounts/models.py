from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .custom_manager import UserCustomManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name=_("username"), max_length=100, unique=True)
    phone_number = models.CharField(
        verbose_name=_("phonenumber"), max_length=11, unique=True
    )
    first_name = models.CharField(verbose_name=_("first name"), max_length=100)
    last_name = models.CharField(verbose_name=_("last name"), max_length=100)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone_number"]

    objects = UserCustomManager()

    def __str__(self):
        return self.username

    @property
    def get_full_name(self):
        return self.first_name + " " + self.last_name
