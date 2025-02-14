from rest_framework import serializers
from .models import Enrollment
from courses.serializers import CourseSerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()  # ✅ Modify this to explicitly pass request

    class Meta:
        model = Enrollment
        fields = ["enrollment_id", "course", "enrolled_at"]

    def get_course(self, obj):
        """Ensures `CourseSerializer` gets `request` context for full thumbnail URL."""
        request = self.context.get("request")  # ✅ Get the request context
        return CourseSerializer(obj.course, context={"request": request}).data  # ✅ Pass request explicitly
