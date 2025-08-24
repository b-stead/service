from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
import uuid


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.OneToOneField(
        "CustomUser",
        on_delete=models.CASCADE,
        related_name="owned_company",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class UserRole(models.TextChoices):
        STAFF = "STF", "Staff"
        SUPPORT = "SUP", "Support"
        RESEARCH = "RES", "Research"
        LEAD = "LED", "Lead"
        COMPANY_OWNER = "CMP", "Company Owner"
        OWNER = "OWN", "Owner"

    role = models.CharField(
        _("User Role"), max_length=3, choices=UserRole.choices, default=UserRole.OWNER
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    sub = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, related_name="staff", null=True, blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    is_deleted = models.BooleanField(default=False)
    deleted_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
