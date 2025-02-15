from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import get_object_or_404
from courses.models import Course
from aggregated_api.serializers import GlobalCourseSerializer, EnrolledCourseSerializer
from enrollments.models import Enrollment
from rest_framework import status


class GlobalCourseView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, course_id):
        # Fetch a single course by ID along with related data
        course = get_object_or_404(
            Course.objects.prefetch_related('category', 'modules', 'modules__lessons'),
            course_id=course_id
        )

        serializer = GlobalCourseSerializer(course)
        return Response(serializer.data)


class EnrolledCourseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        # Check if the user is enrolled in the course
        is_enrolled = Enrollment.objects.filter(user=request.user, course_id=course_id).exists()

        if not is_enrolled:
            return Response(
                {"error": "You are not enrolled in this course."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Fetch the course along with all related data
        course = get_object_or_404(
            Course.objects.prefetch_related('category', 'modules', 'modules__lessons'),
            course_id=course_id
        )

        serializer = EnrolledCourseSerializer(course)
        return Response(serializer.data)
