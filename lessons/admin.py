from django.contrib import admin
from .models import Lesson, LessonVideo, LessonResource
from modules.models import Module

class LessonVideoInline(admin.TabularInline):
    model = LessonVideo
    extra = 1

class LessonResourceInline(admin.TabularInline):
    model = LessonResource
    extra = 1

class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_id', 'title', 'module', 'get_course', 'order', 'created_at')
    list_filter = ('module', 'module__course', 'created_at')
    search_fields = ('title', 'module__title', 'module__course__title')

    inlines = [LessonVideoInline, LessonResourceInline]

    def get_course(self, obj):
        return obj.module.course.title

    get_course.short_description = "Course"

    fieldsets = (
        (None, {
            'fields': ('module', 'title', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Lesson, LessonAdmin)
