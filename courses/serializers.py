from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.SerializerMethodField()
    instructor_id = serializers.IntegerField(source='user.id', read_only=True)  # Rename `user` to `instructor_id`

    class Meta:
        model = Course
        fields = [
            "course_id", "instructor_id", "instructor_name", "title", 
            "description", "price", "thumbnail", "created_at", 
            "updated_at", "category"
        ]  # Excluding `user` and adding `instructor_id`
    
    def get_instructor_name(self, obj):
        """Get full name of the instructor (user)"""
        return f"{obj.user.first_name} {obj.user.last_name}"
