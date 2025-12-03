from django.contrib import admin
from .models import AdminProfile

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'is_senior_reviewer')
    list_filter = ('role', 'department', 'is_senior_reviewer')
    search_fields = ('user__username', 'role', 'department')