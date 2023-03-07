# django
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models

# rest framework auth
from rest_framework_simplejwt.tokens import RefreshToken



class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email Address", unique=True)
    first_name = models.CharField("First Name", max_length=30, blank=True)
    last_name = models.CharField("Last Name", max_length=30, blank=True)
    middle_name = models.CharField("Middle Name", max_length=30, blank=True)
    date_joined = models.DateTimeField("Date Joined", auto_now_add=True)
    is_verified = models.BooleanField(default=True)
    is_active = models.BooleanField("Active", default=True)
    is_staff = models.BooleanField("Staff Status", default=False)
    phone = models.CharField(max_length=17)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        if self.first_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return self.email


    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

