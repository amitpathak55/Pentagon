from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    Group
)
from django.contrib.auth.models import PermissionsMixin

class AdminUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
            Creates and saves a New User
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class AdminUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email Address',
        max_length=255,
        unique=True
    )
    first_name = models.CharField(verbose_name='First Name', max_length=255)
    last_name = models.CharField(
        verbose_name='Last Name',
        max_length=255,
        null=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    group_id = models.ForeignKey(
        Group,
        verbose_name='Group',
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    object = AdminUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        if self.is_admin:
            return False
        return True
