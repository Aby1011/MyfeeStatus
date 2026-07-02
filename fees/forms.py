from django import forms
from .models import FeeStructure, StudentFee, FeeReminder
from accounts.models import Student

class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['name', 'description', 'course', 'year', 'semester', 'amount', 'due_date', 'late_fee_amount']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'late_fee_amount': forms.NumberInput(attrs={'step': '0.01'}),
        }

class StudentFeeForm(forms.ModelForm):
    class Meta:
        model = StudentFee
        fields = ['student', 'fee_structure', 'total_amount', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'total_amount': forms.NumberInput(attrs={'step': '0.01'}),
        }

class FeeReminderForm(forms.ModelForm):
    class Meta:
        model = FeeReminder
        fields = ['student_fee', 'reminder_date', 'message']
        widgets = {
            'reminder_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'message': forms.Textarea(attrs={'rows': 4}),
        }

class FeeSearchForm(forms.Form):
    COURSE_CHOICES = [('', 'All Courses')] + FeeStructure.COURSE_CHOICES
    STATUS_CHOICES = [('', 'All Status')] + StudentFee.STATUS_CHOICES
    
    student_id = forms.CharField(max_length=20, required=False, 
                                widget=forms.TextInput(attrs={'placeholder': 'Student ID'}))
    course = forms.ChoiceField(choices=COURSE_CHOICES, required=False)
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    year = forms.ChoiceField(choices=[('', 'All Years')] + FeeStructure.YEAR_CHOICES, required=False)
