from django.contrib import admin
from django.utils.html import format_html
from .models import Course
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the custom user model

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'title', 'category', 'instructor', 'price', 'created_at', 'updated_at')
    search_fields = ('title', 'category__category_name', 'user__first_name', 'user__last_name')
    list_filter = ('category', 'user', 'created_at')
    ordering = ('created_at',)
    fields = ('category', 'user', 'title', 'description', 'price', 'thumbnail')
    readonly_fields = ('created_at', 'updated_at')

    # Custom method to display "Instructor" in the admin list view
    def instructor(self, obj):
        return format_html(f'{obj.user.first_name} {obj.user.last_name}')
    
    instructor.short_description = "Instructor"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].label = "Instructor"
        return form

    def get_queryset(self, request):
        """Override to filter courses based on user permissions."""
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter the user field to only show users with the 'Instructor' role."""
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role="instructor")  # Ensure only instructors are selectable
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Course, CourseAdmin)
