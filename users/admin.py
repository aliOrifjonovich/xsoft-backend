from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User,UserRole

@admin.register(UserRole)
class BranchAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name"
    ]
# Register your models here.
class UserAdmin(BaseUserAdmin):
    list_display = (
        "phone_number",
        "email",
        "full_name",
        "address",
        "is_staff",
        "user_role",
        "id",
    )
    list_filter = ("is_staff", "user_role")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone_number",
                    "email",
                    "full_name",
                    "password",
                    "branch",
                    "user_role",
                    "address",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "address",
                    "user_role",
                    "full_name",
                    "phone_number",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("phone_number", "full_name","email")
    ordering = ("phone_number","email")


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)