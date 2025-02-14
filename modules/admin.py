from django.contrib import admin
from .models import Module

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('module_id', 'title', 'course', 'order', 'created_at', 'updated_at')  # Fields to display in the list view
    list_filter = ('course', 'created_at', 'updated_at')  # Filters for the list view
    search_fields = ('title', 'course__title')  # Fields to search in the admin panel
    ordering = ('order',)  # Default ordering by module order

    # Optional: Customize the form layout for add/edit views
    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'order')
        }),
        ('Timestamp Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    # Make 'created_at' and 'updated_at' fields read-only
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Module, ModuleAdmin)
