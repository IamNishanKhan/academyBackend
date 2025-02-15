from django.db import models
from modules.models import Module

class Lesson(models.Model):
    lesson_id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class LessonVideo(models.Model):
    video_id = models.AutoField(primary_key=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="videos")  # ✅ Related to Lesson
    video_title = models.CharField(max_length=255)
    video_link = models.URLField()

    def __str__(self):
        return self.video_title


class LessonResource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="resources")  # ✅ Related to Lesson
    resource_title = models.CharField(max_length=255)
    resource_link = models.URLField()

    def __str__(self):
        return self.resource_title
