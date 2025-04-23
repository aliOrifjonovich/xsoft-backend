from django.contrib import admin


from .models.branch import Branch
from .models.cars import Car,CarImages,CarFeatures,CarCategory
from app.models.notification import MessageLog
from app.models.employee import Employee
from app.models.client import Client


@admin.register(CarCategory)
class CarCategory(admin.ModelAdmin):
    list_display = [
        "id",
        "name"
    ]

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "fullname"
    ]
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "fullname"
    ]
@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "send_by"
    ]
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name"
    ]
@admin.register(CarFeatures)
class CarFeatureAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name"
    ]

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "brand"
    ]
@admin.register(CarImages)
class CarAdminAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "car_id"
    ]