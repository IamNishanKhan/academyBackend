from django.contrib import admin
from .models import Lesson
from modules.models import Module  # Import the Module model

class ModuleAdminDisplay(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('course')  # Optimize DB query

    def display_module_with_course(self, obj):
        return f"{obj.title} - {obj.course.title}"  # Show "Module Name - Course Name"

    display_module_with_course.short_description = "Module (Course)"  # Rename column in admin panel

class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_id', 'title', 'module', 'get_course', 'duration', 'order', 'created_at')
    list_filter = ('module', 'module__course', 'created_at')  # Add course filter
    search_fields = ('title', 'module__title', 'module__course__title')  # Search modules & courses

    # Custom method to show Course Name
    def get_course(self, obj):
        return obj.module.course.title  # Get course name from module

    get_course.short_description = "Course"  # Rename column in admin panel

    fieldsets = (
        (None, {
            'fields': ('module', 'title', 'video_url', 'duration', 'order')
        }),
        ('Timestamp Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Lesson, LessonAdmin)
