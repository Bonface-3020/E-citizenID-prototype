from django.contrib import admin
from .models import IDApplication


@admin.register(IDApplication)
class IDApplicationAdmin(admin.ModelAdmin):
    # Fields to display in the main list view
    list_display = ('full_name', 'application_type', 'status', 'applicant', 'date_submitted')

    # Filters in the sidebar
    list_filter = ('application_type', 'status', 'date_submitted')

    # Search fields for the search bar
    search_fields = ('full_name', 'email', 'old_id_number', 'guardian_name')

    # Grouping fields in the detail view for better organization
    fieldsets = (
        ('Application Status', {
            'fields': ('applicant', 'application_type', 'status'),
            'description': 'Core tracking information.'
        }),
        ('Personal Details', {
            'fields': ('full_name', 'phone_number', 'email', 'passport_picture'),
        }),
        ('New ID Details (If Applicable)', {
            'fields': ('county_of_birth', 'subcounty_of_birth', 'location_of_birth', 'sublocation_of_birth'),
            'classes': ('collapse',),  # Makes this section collapsible
        }),
        ('Guardian/Parent Details', {
            'fields': ('guardian_name', 'guardian_id_number', 'guardian_phone', 'death_certificate_number'),
            'classes': ('collapse',),
        }),
        ('Replacement Details (If Applicable)', {
            'fields': ('old_id_number', 'police_abstract_form'),
            'classes': ('collapse',),
        }),
    )