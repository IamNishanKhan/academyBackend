from rest_framework import viewsets, permissions
from .models import Enrollment
from .serializers import EnrollmentSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensures only authenticated users access

    def get_queryset(self):
        """Filter enrollments to show only those belonging to the authenticated user"""
        return Enrollment.objects.filter(user=self.request.user)
