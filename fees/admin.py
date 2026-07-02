from django.contrib import admin
from .models import FeeStructure, StudentFee, FeeReminder

class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'year', 'semester', 'amount', 'due_date', 'is_active')
    list_filter = ('course', 'year', 'semester', 'is_active', 'due_date')
    search_fields = ('name', 'description')
    ordering = ['-created_at']

class StudentFeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_structure', 'amount_paid', 'status', 'due_date', 'updated_at')
    list_filter = ('status', 'due_date', 'created_at')
    search_fields = ('student__user__username', 'student__student_id', 'fee_structure__name')
    ordering = ['-updated_at']

class FeeReminderAdmin(admin.ModelAdmin):
    list_display = ('student_fee', 'reminder_date', 'message', 'is_sent')
    list_filter = ('is_sent', 'reminder_date')
    search_fields = ('student_fee__student__user__username', 'message')
    ordering = ['-reminder_date']

admin.site.register(FeeStructure, FeeStructureAdmin)
admin.site.register(StudentFee, StudentFeeAdmin)
admin.site.register(FeeReminder, FeeReminderAdmin)
