from django.db import models
from django.utils import timezone

class User(models.Model):
    title = models.CharField(max_length=255, default = "Untitled")
    content = models.TextField(blank = True)
    author = models.CharField(max_length=100, default="Anonymous")
    created_at = models.DateTimeField(default = timezone.now)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title
