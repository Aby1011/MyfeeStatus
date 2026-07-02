from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.utils import timezone
from .models import FeeStructure, StudentFee, FeeReminder
from .forms import FeeStructureForm, StudentFeeForm, FeeReminderForm, FeeSearchForm
from accounts.models import Student

@login_required
def fee_list(request):
    form = FeeSearchForm(request.GET)
    fees = StudentFee.objects.all()
    
    if request.user.is_student():
        try:
            fees = fees.filter(student=request.user.student)
        except Student.DoesNotExist:
            return redirect('accounts:student_profile')
    
    if form.is_valid():
        if form.cleaned_data['student_id']:
            fees = fees.filter(student__student_id__icontains=form.cleaned_data['student_id'])
        if form.cleaned_data['course']:
            fees = fees.filter(student__course=form.cleaned_data['course'])
        if form.cleaned_data['status']:
            fees = fees.filter(status=form.cleaned_data['status'])
        if form.cleaned_data['year']:
            fees = fees.filter(student__year=form.cleaned_data['year'])
    
    # Update overdue fees
    for fee in fees:
        if fee.is_overdue and fee.status != 'paid':
            fee.apply_late_fee()
            fee.update_status()
    
    context = {
        'fees': fees,
        'form': form,
        'title': 'Fee Management'
    }
    return render(request, 'fees/fee_list.html', context)

@login_required
def fee_structure_list(request):
    if not (request.user.is_admin() or request.user.is_finance_manager()):
        messages.error(request, 'Access denied. Only admins and finance managers can view fee structures.')
        return redirect('dashboard:home')
    
    structures = FeeStructure.objects.all()
    return render(request, 'fees/structure_list.html', {'structures': structures})

@login_required
def fee_structure_create(request):
    if not (request.user.is_admin() or request.user.is_finance_manager()):
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = FeeStructureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee structure created successfully!')
            return redirect('fees:structure_list')
    else:
        form = FeeStructureForm()
    
    return render(request, 'fees/structure_form.html', {'form': form, 'title': 'Create Fee Structure'})

@login_required
def fee_structure_edit(request, pk):
    if not (request.user.is_admin() or request.user.is_finance_manager()):
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    
    structure = get_object_or_404(FeeStructure, pk=pk)
    
    if request.method == 'POST':
        form = FeeStructureForm(request.POST, instance=structure)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee structure updated successfully!')
            return redirect('fees:structure_list')
    else:
        form = FeeStructureForm(instance=structure)
    
    return render(request, 'fees/structure_form.html', {'form': form, 'title': 'Edit Fee Structure'})

@login_required
def fee_structure_delete(request, pk):
    if not (request.user.is_admin() or request.user.is_finance_manager()):
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    
    structure = get_object_or_404(FeeStructure, pk=pk)
    
    if request.method == 'POST':
        structure.delete()
        messages.success(request, 'Fee structure deleted successfully!')
        return redirect('fees:structure_list')
    
    return render(request, 'fees/structure_confirm_delete.html', {'structure': structure})

@login_required
def assign_fees(request):
    if not (request.user.is_admin() or request.user.is_finance_manager()):
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        structure_id = request.POST.get('fee_structure')
        student_ids = request.POST.getlist('students')
        
        if structure_id and student_ids:
            structure = get_object_or_404(FeeStructure, pk=structure_id)
            created_count = 0
            
            for student_id in student_ids:
                student = get_object_or_404(Student, pk=student_id)
                
                # Check if fee already exists
                if not StudentFee.objects.filter(student=student, fee_structure=structure).exists():
                    StudentFee.objects.create(
                        student=student,
                        fee_structure=structure,
                        total_amount=structure.amount,
                        due_date=structure.due_date
                    )
                    created_count += 1
            
            messages.success(request, f'Fees assigned to {created_count} students successfully!')
            return redirect('fees:assign')
    
    structures = FeeStructure.objects.filter(is_active=True)
    students = Student.objects.all()
    
    return render(request, 'fees/assign_fees.html', {
        'structures': structures,
        'students': students
    })

@login_required
def student_fee_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    
    # Check permissions
    if request.user.is_student() and request.user.student != student:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    
    fees = StudentFee.objects.filter(student=student)
    total_pending = fees.filter(status__in=['pending', 'overdue', 'partial']).aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    return render(request, 'fees/student_detail.html', {
        'student': student,
        'fees': fees,
        'total_pending': total_pending
    })

@login_required
def reminder_list(request):
    if not (request.user.is_admin() or request.user.is_finance_manager()):
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    
    reminders = FeeReminder.objects.all()
    return render(request, 'fees/reminder_list.html', {'reminders': reminders})

@login_required
def create_reminder(request):
    if not (request.user.is_admin() or request.user.is_finance_manager()):
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = FeeReminderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reminder created successfully!')
            return redirect('fees:reminder_list')
    else:
        form = FeeReminderForm()
    
    return render(request, 'fees/reminder_form.html', {'form': form})

@login_required
def overdue_fees(request):
    if not (request.user.is_admin() or request.user.is_finance_manager()):
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    
    overdue_fees = StudentFee.objects.filter(
        due_date__lt=timezone.now().date(),
        status__in=['pending', 'partial', 'overdue']
    )
    
    # Apply late fees and update status
    for fee in overdue_fees:
        fee.apply_late_fee()
        fee.update_status()
    
    return render(request, 'fees/overdue_list.html', {'fees': overdue_fees})