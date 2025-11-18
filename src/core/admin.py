from django.contrib import admin
from .models import Resource 

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("id","title","owner","created_at")
    search_fields = ("title",)
    list_selected_related = ("owner",)

# Register your models here.
