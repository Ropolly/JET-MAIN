"""
Admin configuration for contacts app.
"""
from django.contrib import admin
from .models import Contact, FBO, Ground


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin configuration for Contact model."""
    list_display = ('full_name', 'email', 'phone', 'company', 'contact_type', 'is_active')
    list_filter = ('contact_type', 'is_active', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'company')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth')
        }),
        ('Professional Information', {
            'fields': ('company', 'title', 'contact_type')
        }),
        ('Address & Notes', {
            'fields': ('address', 'notes')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(FBO)
class FBOAdmin(admin.ModelAdmin):
    """Admin configuration for FBO model."""
    list_display = ('name', 'airport_code', 'phone', 'email', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'airport_code', 'phone', 'email', 'services_offered')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'airport_code', 'phone', 'email')
        }),
        ('Services & Details', {
            'fields': ('services_offered', 'operating_hours', 'notes')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Ground)
class GroundAdmin(admin.ModelAdmin):
    """Admin configuration for Ground model."""
    list_display = ('company_name', 'airport_code', 'contact_person', 'phone', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('company_name', 'airport_code', 'contact_person', 'phone', 'services')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Company Information', {
            'fields': ('company_name', 'airport_code', 'contact_person', 'phone', 'email')
        }),
        ('Services & Details', {
            'fields': ('services', 'equipment', 'notes')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
