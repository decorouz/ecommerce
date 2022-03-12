from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django_countries.fields import CountryField

# Create your models here.


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, user_name, password, **other_fields):
        """
        Creates and saves a superuser with the given email, username, password and other fields
        """
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_superuser", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True")

        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True")

        user = self.create_user(email, user_name, password, **other_fields)
        return user

    def create_user(self, email, user_name, password, **other_fields):
        """
        Creates and saves a User with the given email, username, password and other fields required
        """
        if not email:
            raise ValueError(_("User must have an email address"))

        user = self.model(email=self.normalize_email(email), user_name=user_name, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    about = models.TextField(_("about"), max_length=500, blank=True)
    country = CountryField(blank_label='(select country)', blank=True)
    phone_number = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name"]

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def __str__(self) -> str:
        return self.user_name

    def get_name(self):
        return self.first_name
