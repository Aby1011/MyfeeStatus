from django.db import models
from django.utils import timezone
from fees.models import StudentFee
import uuid
import random
import string

class Payment(models.Model):
    PAYMENT_MODE_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('upi', 'UPI'),
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    student_fee = models.ForeignKey(StudentFee, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    reference_number = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Payment gateway details
    gateway_response = models.JSONField(default=dict, blank=True)
    
    # Card/UPI details (for display purposes only - never store sensitive data)
    masked_card_number = models.CharField(max_length=20, blank=True)
    card_holder_name = models.CharField(max_length=100, blank=True)
    upi_id = models.CharField(max_length=100, blank=True)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_transaction_id()
        super().save(*args, **kwargs)
    
    def generate_transaction_id(self):
        """Generate a unique transaction ID"""
        prefix = 'TXN'
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"{prefix}{timestamp}{random_part}"
    
    def process_payment(self):
        """Simulate payment processing"""
        self.status = 'processing'
        self.save()
        
        # Simulate payment gateway response
        import time
        import random
        
        # Simulate processing delay
        time.sleep(1)
        
        # 95% success rate for simulation
        if random.random() < 0.95:
            self.status = 'completed'
            self.processed_at = timezone.now()
            self.gateway_response = {
                'status': 'success',
                'gateway_transaction_id': f"GW{random.randint(100000, 999999)}",
                'message': 'Payment processed successfully'
            }
            
            # Update student fee
            self.student_fee.amount_paid += self.amount
            self.student_fee.update_status()
            
        else:
            self.status = 'failed'
            self.gateway_response = {
                'status': 'failed',
                'error_code': 'E001',
                'message': 'Payment processing failed. Please try again.'
            }
        
        self.save()
        return self.status == 'completed'
    
    def __str__(self):
        return f"{self.transaction_id} - {self.student_fee.student.student_id} - ${self.amount}"
    
    class Meta:
        ordering = ['-created_at']

class PaymentReceipt(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='receipt')
    receipt_number = models.CharField(max_length=50, unique=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = self.generate_receipt_number()
        super().save(*args, **kwargs)
    
    def generate_receipt_number(self):
        """Generate a unique receipt number"""
        prefix = 'RCP'
        timestamp = timezone.now().strftime('%Y%m%d')
        sequence = PaymentReceipt.objects.filter(
            generated_at__date=timezone.now().date()
        ).count() + 1
        return f"{prefix}{timestamp}{sequence:04d}"
    
    def __str__(self):
        return f"Receipt {self.receipt_number} for {self.payment.transaction_id}"
    
    class Meta:
        ordering = ['-generated_at']
