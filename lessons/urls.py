from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LessonViewSet, LessonVideoViewSet, LessonResourceViewSet

router = DefaultRouter()
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'lesson-videos', LessonVideoViewSet, basename='lesson-video')
router.register(r'lesson-resources', LessonResourceViewSet, basename='lesson-resource')

urlpatterns = [
    path('', include(router.urls)),
]
