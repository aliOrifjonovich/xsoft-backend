from django.db import models
from uuid import uuid4
import os
from app.models.branch import Branch
from users.models import User,UserRole
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


def employee_images_upload_to(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join(f'employee/{instance}/{filename}')


class Employee(models.Model):

    class GENDER_CHOICES(models.TextChoices):
        MALE = "Male", _("Male")
        FEMALE = "Female", _("Female")
    
    class EMPLOYMENT_TYPE_CHOICES(models.TextChoices):
        MALE = "Full_time", _("Full-time")
        PART_TIME= "Part_time",_("Part-time")
        CONTRACT = "Contract", _("Contract")
        
    class WORK_STATUS_CHOICES(models.TextChoices):
        Active="Active",_("Active")
        VACATION="Vacation",_("Vacatio")
        FIRED="Fired",_("Fired")


    photo = models.FileField(upload_to=employee_images_upload_to,null=True,blank=True)
    fullname = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES.choices)
    phone_number_regex = RegexValidator(regex=r"^(\+998|998)\d{9}$", message="Phone number Regex")
    phone_number = models.CharField(validators=[phone_number_regex], max_length=16, unique=True,null=True)    
    position = models.CharField(max_length=100)
    employmentType = models.CharField(max_length=11, choices=EMPLOYMENT_TYPE_CHOICES.choices)
    hireDate = models.DateField()
    branch = models.ForeignKey(Branch,related_name="brach_of_employee", on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    workStatus = models.CharField(max_length=50, choices=WORK_STATUS_CHOICES.choices)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding 
        super().save(*args, **kwargs) 
        if is_new:
            if self.workStatus != self.WORK_STATUS_CHOICES.FIRED:
                try:
                    try:
                        user_role= UserRole.objects.get(name="user")
                    except UserRole.DoesNotExist:
                        user_role = UserRole.objects.create(
                            name="user"
                        )
                    user = User.objects.create(
                    phone_number=self.phone_number,  
                    full_name=self.fullname,
                    user_role=user_role,
                        email=self.user.email if self.user else None,
                    )

                    # Assign branches after the user is created
                    if self.branch:  # Ensure branches exist before assigning
                        user.branch.set(self.branch) 
                        user.save()
                    self.user = user
                    self.save()
                except IntegrityError as e:
                    print(f"Failed to create user: {e}")
                except ValidationError as e:
                    print(f"Validation error: {e}")


    def __str__(self):
        return self.fullname