from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name', 'created_at')  # Fields to display in the list view
    search_fields = ('category_name',)  # Allow search by category name
    list_filter = ('created_at',)  # Filter by creation date
    ordering = ('created_at',)  # Order by creation date by default
    fields = ('category_name',)  # Specify fields to display in the edit form (category_name is editable)

admin.site.register(Category, CategoryAdmin)
