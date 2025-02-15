from django.contrib import admin
from django.utils.html import format_html
from .models import Course, CourseOutcome, CoursePrerequisite
from django.contrib.auth import get_user_model

User = get_user_model()

class CourseOutcomeInline(admin.TabularInline):
    model = CourseOutcome
    extra = 1

class CoursePrerequisiteInline(admin.TabularInline):
    model = CoursePrerequisite
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'title', 'category', 'instructor', 'price', 'created_at', 'updated_at')
    search_fields = ('title', 'category__category_name', 'user__first_name', 'user__last_name')
    list_filter = ('category', 'user', 'created_at')
    ordering = ('created_at',)
    inlines = [CourseOutcomeInline, CoursePrerequisiteInline]

    fieldsets = (
        (None, {
            'fields': ('category', 'user', 'title', 'description', 'price', 'thumbnail')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def instructor(self, obj):
        return format_html(f'{obj.user.first_name} {obj.user.last_name}')
    
    instructor.short_description = "Instructor"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].label = "Instructor"
        return form

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role="instructor")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Course, CourseAdmin)
