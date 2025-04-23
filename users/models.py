import os
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from app.models.branch import Branch

# Create your models here.
def avatar_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("avatar/", filename)

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number field must be set")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)


class UserRole(models.Model):
    name = models.CharField(max_length=255)
    # access = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

class User(AbstractUser):
    email = models.EmailField(null=True,blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    branch = models.ManyToManyField(Branch, blank=True)
    user_role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, related_name="role", null=True, blank=True)
    avatar = models.FileField(upload_to=avatar_path, null=True, blank=True,validators=[])
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number_regex = RegexValidator(regex=r"^(\+998|998)\d{9}$", message="Phone number Regex")
    comment = models.CharField(max_length=255,null=True,blank=True)
    phone_number = models.CharField(validators=[phone_number_regex], max_length=16, unique=True,null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otp_counter = models.PositiveSmallIntegerField(default=0)
    otp_sent_time = models.DateTimeField(null=True, blank=True)
    otp_tried = models.BooleanField(default=False)
    
    USERNAME_FIELD = "phone_number"
    username = None
    first_name = None
    last_name = None

    objects = CustomUserManager()

    class Meta:
        db_table = "users"
    
    def __str__(self) -> str:
        return self.phone_number if self.phone_number else "Unnamed User"
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class UniqueConfig(models.Model):
    otp_counter = models.PositiveIntegerField(default=0)

