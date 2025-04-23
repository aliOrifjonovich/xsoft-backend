from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class Client(models.Model):
    class STATUS_CHOICES(models.TextChoices):
        Active="Active",_("Active")
        InActive="InActive",_("InActive")
        BLACKLISTED="Blacklisted",_("Blacklisted")

    fullname = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True,unique=True)
    phone_number_regex = RegexValidator(regex=r"^(\+998|998)\d{9}$", message="Phone number Regex")
    phone_number = models.CharField(validators=[phone_number_regex], max_length=16, unique=True,null=True)
    address = models.CharField(max_length=255)
    passportid = models.CharField(max_length=255,unique=True)
    driverLicense = models.CharField(max_length=255,unique=True)
    licenseExpiry = models.DateField()
    age = models.IntegerField()
    status = models.CharField(max_length=11, choices=STATUS_CHOICES.choices)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return f"{self.phone_number}"
