from django.db import models
from uuid import uuid4
import os
from ..models.branch import Branch
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

def car_images_upload_to(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join(f'cars/{instance}/{filename}')

class CarCategory(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

class CarFeatures(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"
    

class Car(models.Model):
    class COLOR_CHOICES(models.TextChoices):
        RED = "red", _("Red")
        BLUE = "blue", _("Blue")
        BLACK = "black", _("Black")
        WHITE = "white", _("White")
        SILVER = "silver", _("Silver")
        GRAY = "gray", _("Gray")

    class FUEL_CHOICES(models.TextChoices):
        DIESEL = "diesel", _("Diesel")
        PETROL = "petrol", _("Petrol")
        ELECTRIC = "electric", _("Electric")
        HYBRID = "hybrid", _("Hybrid")

    class ENGINE_CHOICES(models.TextChoices):
        ENGINE_0_6L = "0.6L", _("0.6L")
        ENGINE_1_0L = "1.0L", _("1.0L")
        ENGINE_1_5L = "1.5L", _("1.5L")
        ENGINE_2_0L = "2.0L", _("2.0L")
        ENGINE_2_5L = "2.5L", _("2.5L")
        ENGINE_3_0L = "3.0L", _("3.0L")
        ENGINE_3_5L = "3.5L", _("3.5L")
        ENGINE_4_0L = "4.0L", _("4.0L")
        ENGINE_5_0L = "5.0L", _("5.0L")
        ENGINE_6_0L = "6.0L", _("6.0L")
        ENGINE_7_0L_PLUS = "7.0L+", _("7.0L+")

    class RENTAL_STATUS_CHOICES(models.TextChoices):
        BOSH = "bosh", _("Bo'sh")
        IJARADA = "ijarada", _("Ijarada")
        RESERV = "reserved", _("Reserv qilingan")

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey("app.CarCategory", on_delete=models.CASCADE, null=True)
    seating_capacity = models.PositiveIntegerField()
    transmission = models.CharField(max_length=50)
    mileage = models.PositiveIntegerField()
    rental_price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    owner_name = models.CharField(max_length=100)
    owner_phone = models.CharField(max_length=20)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES.choices)
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES.choices)
    year = models.PositiveIntegerField()
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_age = models.PositiveIntegerField()
    features = models.ManyToManyField("CarFeatures", blank=True)
    engine_size = models.CharField(max_length=10, choices=ENGINE_CHOICES.choices)
    rental_status = models.CharField(max_length=20, choices=RENTAL_STATUS_CHOICES.choices, default=RENTAL_STATUS_CHOICES.BOSH)
    description = models.TextField(blank=True)
    branch = models.ForeignKey("Branch", related_name="brach_of_car", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"

class CarImages(models.Model):
    photo = models.FileField(upload_to=car_images_upload_to)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")

    def __str__(self) -> str:
        return f"{self.car_id}"