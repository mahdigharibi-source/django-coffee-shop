from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from accounts.managers import UserManager


class UserType(models.TextChoices):
    SUPERUSER = "superuser", _("Superuser")
    ADMIN = "admin", _("Admin")
    CUSTOMER = "customer", _("Customer")


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email"), max_length=255, unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_verified = models.BooleanField(default=False)

    user_type = models.CharField(choices=UserType.choices, default=UserType.CUSTOMER)

    datetime_create = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)
    #profile
    #comments
    #addresses
    #cart

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11, validators=[
        RegexValidator(
            regex=r'^\d{11}$',
            message="Phone number must be exactly 11 digits"
        )
    ])

    datetime_create = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name



