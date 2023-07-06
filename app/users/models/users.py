from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from core.utils.models import TimeStampModel


class UserbaseManager(BaseUserManager):

    def create_superuser(self, email, first_name, password, **other_fields):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, first_name, password, **other_fields)

    def create_user(self, email, first_name, password, **other_fields):

        if not email:
            raise ValueError("You must provide an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


def image_directory_path(instance, filename):
    return "users/{0}/profile_image.jpg".format(instance.email)


class UserBase(AbstractBaseUser, PermissionsMixin, TimeStampModel):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150)

    contact = models.CharField(max_length=15, null=True, blank=True)
    profile_image = models.ImageField(upload_to=image_directory_path,
                                      null=True,
                                      blank=True)

    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    objects = UserbaseManager()

    def __str__(self):
        return f"{self.email}"

    class Meta:
        ordering = ["-id"]


class UserProfile(TimeStampModel, models.Model):
    userbase = models.OneToOneField(UserBase,
                                    on_delete=models.CASCADE,
                                    related_name='profile')
    distance_ran = models.DecimalField(default=0.0,
                                       max_digits=60,
                                       decimal_places=2)

    def __str__(self):
        return f"{self.userbase.email}"
