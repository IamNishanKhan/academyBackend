from django.contrib import admin
from .models import Enrollment

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('enrollment_id', 'user', 'course', 'enrolled_at')  # Fields to display in the list view
    list_filter = ('user', 'course', 'enrolled_at')  # Filters for the list view
    search_fields = ('user__first_name', 'user__last_name', 'course__title')  # Fields to search in the admin panel
    ordering = ('-enrolled_at',)  # Default ordering by enrollment date (latest first)

    # Exclude 'enrolled_at' from the form to prevent editing it manually
    exclude = ('enrolled_at',)

admin.site.register(Enrollment, EnrollmentAdmin)
