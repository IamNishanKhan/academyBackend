from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.SerializerMethodField()
    instructor_id = serializers.IntegerField(source='user.id', read_only=True)
    course_title = serializers.CharField(source='title', read_only=True)

    class Meta:
        model = Course
        fields = [
            "course_id", "instructor_id", "instructor_name", "course_title", 
            "description", "price", "thumbnail", "created_at", 
            "updated_at", "category"
        ]
    
    def get_instructor_name(self, obj):
        """Get full name of the instructor (user)"""
        return f"{obj.user.first_name} {obj.user.last_name}"
