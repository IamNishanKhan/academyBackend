from rest_framework import serializers
from courses.models import Course
from modules.models import Module
from lessons.models import Lesson, LessonVideo, LessonResource

class GlobalLessonVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonVideo
        fields = ['video_id', 'lesson_id', 'video_title']

class GlobalLessonResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonResource
        fields = ['resource_id', 'lesson_id', 'resource_title']

class GlobalLessonSerializer(serializers.ModelSerializer):
    module_id = serializers.IntegerField(source='module.module_id')
    lesson_title = serializers.CharField(source='title')
    videos = GlobalLessonVideoSerializer(many=True, read_only=True)
    resources = GlobalLessonResourceSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['lesson_id', 'module_id', 'lesson_title', 'order', 'created_at', 'videos', 'resources']

class GlobalModuleSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(source='course.course_id')
    module_title = serializers.CharField(source='title')
    lessons = GlobalLessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['module_id', 'course_id', 'module_title', 'order', 'lessons']

class GlobalCourseSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='category.category_id')
    category_name = serializers.CharField(source='category.category_name')
    instructor_name = serializers.SerializerMethodField()
    modules = GlobalModuleSerializer(many=True, read_only=True)
    course_title = serializers.CharField(source='title')

    class Meta:
        model = Course
        fields = ['course_id', 'course_title', 'description', 'price', 'category_id', 'category_name', 'instructor_name', 'modules']

    def get_instructor_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

class EnrolledLessonVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonVideo
        fields = ['video_id', 'lesson_id', 'video_title', 'video_link']

class EnrolledLessonResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonResource
        fields = ['resource_id', 'lesson_id', 'resource_title', 'resource_link']

class EnrolledLessonSerializer(serializers.ModelSerializer):
    module_id = serializers.IntegerField(source='module.module_id')
    lesson_title = serializers.CharField(source='title')
    videos = EnrolledLessonVideoSerializer(many=True, read_only=True)
    resources = EnrolledLessonResourceSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['lesson_id', 'module_id', 'lesson_title', 'order', 'created_at', 'videos', 'resources']

class EnrolledModuleSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(source='course.course_id')
    module_title = serializers.CharField(source='title')
    lessons = EnrolledLessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['module_id', 'course_id', 'module_title', 'order', 'lessons']

class EnrolledCourseSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='category.category_id')
    category_name = serializers.CharField(source='category.category_name')
    instructor_name = serializers.SerializerMethodField()
    modules = EnrolledModuleSerializer(many=True, read_only=True)
    course_title = serializers.CharField(source='title')

    class Meta:
        model = Course
        fields = ['course_id', 'course_title', 'description', 'price', 'category_id', 'category_name', 'instructor_name', 'modules']

    def get_instructor_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
