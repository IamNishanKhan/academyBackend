from django.contrib import admin
from .models import Module

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('module_id', 'title', 'course', 'order', 'created_at', 'updated_at')
    list_filter = ('course', 'created_at', 'updated_at')
    search_fields = ('title', 'course__title')
    ordering = ('order',)

    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'order')
        }),
        ('Timestamp Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Module, ModuleAdmin)
