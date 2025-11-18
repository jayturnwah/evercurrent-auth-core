from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Resources(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_resources"
    )
    title = models.CharField(max_length=200)
    data = models.JSONField(default=dict, blank=True) #flexible payload
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} (#{self.pk})"

class Role(models.Model):
    # simple, flexible role labels
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    roles = models.ManyToManyField(Role, blank=True, related_name='users')
