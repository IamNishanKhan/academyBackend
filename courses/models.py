from django.db import models
from categories.models import Category
from accounts.models import User  # Import user model

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")  # Instructor
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class CourseOutcome(models.Model):
    outcome_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="outcomes")
    outcome_title = models.CharField(max_length=255)

    def __str__(self):
        return self.outcome_title


class CoursePrerequisite(models.Model):
    prerequisite_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="prerequisites")
    prerequisite_title = models.CharField(max_length=255)

    def __str__(self):
        return self.prerequisite_title
