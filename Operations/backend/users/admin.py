"""
Admin configuration for users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Role, Permission, Department


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for UserProfile model."""
    list_display = ('user', 'department', 'phone_number', 'hire_date', 'is_active')
    list_filter = ('department', 'is_active', 'hire_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number')
    filter_horizontal = ('roles', 'permissions')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'department', 'phone_number', 'address')
        }),
        ('Employment', {
            'fields': ('hire_date', 'emergency_contact', 'is_active')
        }),
        ('Permissions', {
            'fields': ('roles', 'permissions')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin configuration for Role model."""
    list_display = ('name', 'description', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """Admin configuration for Permission model."""
    list_display = ('name', 'resource', 'action', 'description')
    list_filter = ('resource', 'action')
    search_fields = ('name', 'resource', 'action', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin configuration for Department model."""
    list_display = ('name', 'manager_email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description', 'manager_email')
    readonly_fields = ('created_at', 'updated_at')


# Extend the default User admin to show related profile info
class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    filter_horizontal = ('roles', 'permissions')


class UserAdmin(BaseUserAdmin):
    """Extended User admin with profile inline."""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_department')
    
    def get_department(self, obj):
        """Get user's department from profile."""
        try:
            return obj.userprofile.department.name if obj.userprofile.department else 'No Department'
        except UserProfile.DoesNotExist:
            return 'No Profile'
    get_department.short_description = 'Department'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
