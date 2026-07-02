from django.db import models
from django.conf import settings
from accounts.models import Student
from django.utils import timezone
from decimal import Decimal

class FeeStructure(models.Model):
    COURSE_CHOICES = [
        ('btech', 'B.Tech'),
        ('mtech', 'M.Tech'),
        ('bsc', 'B.Sc'),
        ('msc', 'M.Sc'),
        ('ba', 'B.A'),
        ('ma', 'M.A'),
        ('bcom', 'B.Com'),
        ('mcom', 'M.Com'),
    ]
    
    YEAR_CHOICES = [
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
    ]
    
    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
        (3, 'Semester 3'),
        (4, 'Semester 4'),
        (5, 'Semester 5'),
        (6, 'Semester 6'),
        (7, 'Semester 7'),
        (8, 'Semester 8'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    course = models.CharField(max_length=10, choices=COURSE_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    late_fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_course_display()} Year {self.year} Sem {self.semester}"
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['course', 'year', 'semester', 'name']

class StudentFee(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('partial', 'Partial'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    late_fee_applied = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.student_id} - {self.fee_structure.name}"
    
    @property
    def remaining_amount(self):
        return self.total_amount + self.late_fee_applied - self.amount_paid
    
    @property
    def is_overdue(self):
        return timezone.now().date() > self.due_date and self.status != 'paid'
    
    def update_status(self):
        if self.amount_paid >= self.total_amount + self.late_fee_applied:
            self.status = 'paid'
        elif self.amount_paid > 0:
            self.status = 'partial'
        elif self.is_overdue:
            self.status = 'overdue'
        else:
            self.status = 'pending'
        self.save()
    
    def apply_late_fee(self):
        if self.is_overdue and self.late_fee_applied == 0:
            self.late_fee_applied = self.fee_structure.late_fee_amount
            self.save()
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['student', 'fee_structure']

class FeeReminder(models.Model):
    student_fee = models.ForeignKey(StudentFee, on_delete=models.CASCADE, related_name='reminders')
    reminder_date = models.DateTimeField()
    message = models.TextField()
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reminder for {self.student_fee.student.student_id} - {self.reminder_date}"
    
    class Meta:
        ordering = ['-reminder_date']
