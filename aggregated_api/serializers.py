from rest_framework import serializers
from courses.models import Course
from modules.models import Module
from lessons.models import Lesson


class GlobalLessonSerializer(serializers.ModelSerializer):
    module_id = serializers.IntegerField(source='module.module_id')
    module_title = serializers.CharField(source='module.title')

    class Meta:
        model = Lesson
        fields = ['lesson_id', 'module_id', 'module_title', 'title', 'order', 'created_at']


class GlobalModuleSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(source='course.course_id')  # Added course_id
    lessons = GlobalLessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['module_id', 'course_id', 'title', 'order', 'lessons']


class GlobalCourseSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='category.category_id')
    category_name = serializers.CharField(source='category.category_name')
    instructor_name = serializers.SerializerMethodField()
    modules = GlobalModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['course_id', 'title', 'description', 'price', 'category_id', 'category_name', 'instructor_name', 'modules']

    def get_instructor_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


class EnrolledLessonSerializer(serializers.ModelSerializer):
    module_id = serializers.IntegerField(source='module.module_id')
    module_title = serializers.CharField(source='module.title')

    class Meta:
        model = Lesson
        fields = ['lesson_id', 'module_id', 'module_title', 'title', 'video_url', 'duration', 'order', 'created_at']


class EnrolledModuleSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(source='course.course_id')  # Added course_id
    lessons = EnrolledLessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['module_id', 'course_id', 'title', 'order', 'lessons']


class EnrolledCourseSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='category.category_id')
    category_name = serializers.CharField(source='category.category_name')
    instructor_name = serializers.SerializerMethodField()
    modules = EnrolledModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['course_id', 'title', 'description', 'price', 'category_id', 'category_name', 'instructor_name', 'modules']

    def get_instructor_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
