from django.contrib import admin
from .models import User, Role

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")
    filter_horizontal = ('roles',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id","name")
    search_fields = ("name",)
    

# Register your models here.
