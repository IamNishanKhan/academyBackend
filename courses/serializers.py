from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.SerializerMethodField()
    instructor_id = serializers.IntegerField(source='user.id', read_only=True)
    course_title = serializers.CharField(source='title', read_only=True)
    category_id = serializers.IntegerField(source='category.category_id', read_only=True)
    category_name = serializers.CharField(source='category.category_name', read_only=True)

    class Meta:
        model = Course
        fields = [
            "course_id", "course_title", "instructor_id", "instructor_name",
            "description", "price", "thumbnail", "created_at", "updated_at",
            "category_id", "category_name"
        ]

    def get_instructor_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
