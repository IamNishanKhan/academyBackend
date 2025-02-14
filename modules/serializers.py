from rest_framework import serializers
from .models import Module
from courses.models import Course

class ModuleSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(source='course.course_id')  # Correctly access the course ID
    course_name = serializers.CharField(source='course.title', read_only=True)  # Correctly access the course name

    class Meta:
        model = Module
        fields = ['module_id', 'title', 'order', 'course_id', 'course_name', 'created_at', 'updated_at']
