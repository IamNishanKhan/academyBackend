from django.db import models
from accounts.models import User
from courses.models import Course

class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} enrolled in {self.course.title}"
