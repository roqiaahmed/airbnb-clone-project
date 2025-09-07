from django.contrib import admin

# Register your models here.
from .models import User

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "user_role", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("phone_number", "user_role")}),
    )
