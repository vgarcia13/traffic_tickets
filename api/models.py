import uuid
import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=128, blank=True, null=True)

    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin


class Person(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, null=False, blank=False)
    full_name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f'{self.full_name} ({self.email})'


class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    plate = models.CharField(unique=True, null=False, blank=False, max_length=10)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.datetime.now().year)]
    )
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.brand} {self.model} {self.year} {self.color} (PLATE: {self.plate})'


class Officer(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    person = models.OneToOneField(Person, on_delete=models.CASCADE)

    def __str__(self):
        return f'Officer {self.person.full_name} (ID: {self.id})'


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    reporting_officer = models.ForeignKey(Officer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f'Ticket ID: {self.id} (PLATE: {self.vehicle.plate}, Officer ID: {self.reporting_officer.id}, DateTime: {self.timestamp})'
