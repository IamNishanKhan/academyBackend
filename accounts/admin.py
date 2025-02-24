from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from accounts.models import User
from django.contrib.auth.models import Group


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'phone', 'role', 'is_active', 'is_staff', 'is_verified', 'edit_user')  # Added 'is_verified'
    list_filter = ('role', 'is_staff', 'is_active', 'is_verified')

    fieldsets = (
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'password', 'profile_picture', 'bio')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'is_verified')}),
        ('Important Dates', {'fields': ('last_login', 'updated_at')}), 
    )

    add_fieldsets = (
        ('Create User', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2', 'role', 'is_active', 'is_staff', 'is_verified')}
        ),
    )
    
    readonly_fields = ('last_login', 'updated_at', 'created_at')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('email', 'first_name', 'last_name', 'role')
    filter_horizontal = ('groups', 'user_permissions')

    def edit_user(self, obj):
        """Creates an edit button that redirects to the edit page for the user."""
        url = reverse('admin:accounts_user_change', args=[obj.id])
        return format_html(f'<a class="button" href="{url}">Edit</a>')

    edit_user.short_description = "Edit"
    edit_user.allow_tags = True

admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
