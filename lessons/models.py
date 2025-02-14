from django.db import models
from modules.models import Module

class Lesson(models.Model):
    lesson_id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    duration = models.PositiveIntegerField()  # Duration in seconds
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
