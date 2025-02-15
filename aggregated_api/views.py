from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import get_object_or_404
from courses.models import Course
from enrollments.models import Enrollment
from rest_framework import status

class GlobalCourseView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, course_id):
        from .serializers import GlobalCourseSerializer  

        course = get_object_or_404(
            Course.objects.prefetch_related(
                'category',
                'modules',
                'modules__lessons',
                'modules__lessons__videos',
                'modules__lessons__resources',
                'outcomes',
                'prerequisites'
            ),
            course_id=course_id
        )

        serializer = GlobalCourseSerializer(course)
        return Response(serializer.data)

class EnrolledCourseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        from .serializers import EnrolledCourseSerializer  

        is_enrolled = Enrollment.objects.filter(user=request.user, course_id=course_id).exists()

        if not is_enrolled:
            return Response(
                {"error": "You are not enrolled in this course."},
                status=status.HTTP_403_FORBIDDEN
            )

        course = get_object_or_404(
            Course.objects.prefetch_related(
                'category',
                'modules',
                'modules__lessons',
                'modules__lessons__videos',
                'modules__lessons__resources',
                'outcomes',
                'prerequisites'
            ),
            course_id=course_id
        )

        serializer = EnrolledCourseSerializer(course)
        return Response(serializer.data)
