from rest_framework import serializers
from .models import Lesson, LessonVideo, LessonResource

class LessonVideoSerializer(serializers.ModelSerializer):
    lesson_id = serializers.IntegerField(source='lesson.lesson_id')

    class Meta:
        model = LessonVideo
        fields = ['video_id', 'lesson_id', 'video_title', 'video_link']


class LessonResourceSerializer(serializers.ModelSerializer):
    lesson_id = serializers.IntegerField(source='lesson.lesson_id')

    class Meta:
        model = LessonResource
        fields = ['resource_id', 'lesson_id', 'resource_title', 'resource_link']


class LessonSerializer(serializers.ModelSerializer):
    videos = LessonVideoSerializer(many=True, read_only=True)
    resources = LessonResourceSerializer(many=True, read_only=True)
    lesson_title = serializers.CharField(source='title', read_only=True)
    module_id = serializers.IntegerField(source='module.module_id', read_only=True)
    module_title = serializers.CharField(source='module.title', read_only=True)

    class Meta:
        model = Lesson
        fields = ['lesson_id', 'module_id', 'module_title', 'lesson_title', 'order', 'created_at', 'videos', 'resources']
