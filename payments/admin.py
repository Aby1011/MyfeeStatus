from django.contrib import admin
from .models import Payment, PaymentReceipt

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'student_fee', 'amount', 'payment_mode', 'status', 'created_at')
    list_filter = ('payment_mode', 'status', 'created_at')
    search_fields = ('transaction_id', 'student_fee__student__student_id', 'student_fee__student__user__username')
    readonly_fields = ('transaction_id', 'created_at', 'updated_at')
    ordering = ['-created_at']

class PaymentReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'payment', 'generated_at', 'is_sent')
    list_filter = ('is_sent', 'generated_at')
    search_fields = ('receipt_number', 'payment__transaction_id')
    readonly_fields = ('receipt_number', 'generated_at')
    ordering = ['-generated_at']

admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentReceipt, PaymentReceiptAdmin)
