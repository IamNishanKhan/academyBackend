from rest_framework import viewsets
from .models import Lesson, LessonVideo, LessonResource
from .serializers import LessonSerializer, LessonVideoSerializer, LessonResourceSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.prefetch_related('videos', 'resources').all()
    serializer_class = LessonSerializer


class LessonVideoViewSet(viewsets.ModelViewSet):
    queryset = LessonVideo.objects.all()
    serializer_class = LessonVideoSerializer


class LessonResourceViewSet(viewsets.ModelViewSet):
    queryset = LessonResource.objects.all()
    serializer_class = LessonResourceSerializer
