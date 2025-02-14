from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .models import Course
from .serializers import CourseSerializer

class ReadOnly(AllowAny):
    def has_permission(self, request, view):
        return request.method in ('GET', 'HEAD', 'OPTIONS')

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [ReadOnly]

    def get_permissions(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return [permission() for permission in self.permission_classes]
        return [IsAuthenticatedOrReadOnly()]
