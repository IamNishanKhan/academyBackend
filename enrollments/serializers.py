from rest_framework import serializers
from .models import Enrollment
from courses.serializers import CourseSerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = ["enrollment_id", "course", "enrolled_at"]

    def get_course(self, obj):
        request = self.context.get("request")
        return CourseSerializer(obj.course, context={"request": request}).data
