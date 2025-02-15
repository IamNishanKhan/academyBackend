from rest_framework import serializers
from .models import Module
from courses.models import Course

class ModuleSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(source='course.course_id')
    course_name = serializers.CharField(source='course.title', read_only=True)
    module_title = serializers.CharField(source='title', read_only=True)

    class Meta:
        model = Module
        fields = ['module_id', 'module_title', 'order', 'course_id', 'course_name', 'created_at', 'updated_at']
