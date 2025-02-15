from django.contrib import admin
from .models import Enrollment

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('enrollment_id', 'user', 'course', 'enrolled_at')
    list_filter = ('user', 'course', 'enrolled_at')
    search_fields = ('user__first_name', 'user__last_name', 'course__title')
    ordering = ('-enrolled_at',)
    exclude = ('enrolled_at',)

admin.site.register(Enrollment, EnrollmentAdmin)
