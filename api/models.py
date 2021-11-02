from django.db import models
from backend.settings import MEDIA_ROOT

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=500)
    desc = models.TextField(max_length=10000, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class MailchimpEmail(models.Model):
    email = models.EmailField(max_length=511)

    def __str__(self):
        return self.email