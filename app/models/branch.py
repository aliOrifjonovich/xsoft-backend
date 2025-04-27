from django.db import models
from uuid import uuid4
import os,random, string


# Create your models here.
def corporation_logo_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("corporation-logo/", filename)

class Branch(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=355)
    status = models.BooleanField(default=True)
    year_of_construction = models.DateField(null=True,default=None)
    total_area = models.FloatField(default=10)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)    
    google_map_link = models.CharField(max_length=255,null=True,blank=True)
    yandex_map_link = models.CharField(max_length=255,null=True,blank=True)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return self.name