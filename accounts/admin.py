from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Student

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_active', 'date_joined')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'email')}),
    )

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'course', 'year', 'semester', 'parent_contact')
    list_filter = ('course', 'year', 'semester')
    search_fields = ('user__username', 'student_id', 'user__email')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
