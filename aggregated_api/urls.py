from django.urls import path
from .views import GlobalCourseView, EnrolledCourseDetailView

urlpatterns = [
    path('course-details/<int:course_id>/', GlobalCourseView.as_view(), name='single-course'),
    path('enrolled-course/<int:course_id>/', EnrolledCourseDetailView.as_view(), name='full-course-detail'),
]
