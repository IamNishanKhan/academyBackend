from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name', 'created_at')
    search_fields = ('category_name',)
    list_filter = ('created_at',)
    ordering = ('created_at',)
    fields = ('category_name',)

admin.site.register(Category, CategoryAdmin)
