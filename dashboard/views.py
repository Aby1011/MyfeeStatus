from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from accounts.models import CustomUser, Student
from fees.models import StudentFee, FeeStructure
from payments.models import Payment

@login_required
def dashboard_home(request):
    """Route users to appropriate dashboard based on user type"""
    if request.user.is_admin():
        return redirect('dashboard:admin')
    elif request.user.is_finance_manager():
        return redirect('dashboard:finance')
    elif request.user.is_student():
        return redirect('dashboard:student')
    else:
        return render(request, 'dashboard/home.html')

@login_required
def admin_dashboard(request):
    """Admin dashboard with comprehensive statistics"""
    if not request.user.is_admin():
        return redirect('dashboard:home')
    
    # User statistics
    total_users = CustomUser.objects.count()
    total_students = Student.objects.count()
    total_finance_managers = CustomUser.objects.filter(user_type='finance_manager').count()
    
    # Fee statistics
    total_fees = StudentFee.objects.count()
    pending_fees = StudentFee.objects.filter(status__in=['pending', 'overdue']).count()
    paid_fees = StudentFee.objects.filter(status='paid').count()
    
    # Payment statistics
    total_payments = Payment.objects.filter(status='completed').count()
    total_revenue = Payment.objects.filter(status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Recent activities
    recent_payments = Payment.objects.filter(status='completed').order_by('-created_at')[:10]
    recent_students = Student.objects.order_by('-user__date_joined')[:10]
    
    # Overdue fees
    overdue_fees = StudentFee.objects.filter(
        due_date__lt=timezone.now().date(),
        status__in=['pending', 'overdue']
    ).count()
    
    context = {
        'total_users': total_users,
        'total_students': total_students,
        'total_finance_managers': total_finance_managers,
        'total_fees': total_fees,
        'pending_fees': pending_fees,
        'paid_fees': paid_fees,
        'total_payments': total_payments,
        'total_revenue': total_revenue,
        'recent_payments': recent_payments,
        'recent_students': recent_students,
        'overdue_fees': overdue_fees,
        'title': 'Admin Dashboard'
    }
    return render(request, 'dashboard/admin.html', context)

@login_required
def finance_dashboard(request):
    """Finance manager dashboard with payment and fee management focus"""
    if not request.user.is_finance_manager():
        return redirect('dashboard:home')
    
    # Payment statistics
    today = timezone.now().date()
    payments_today = Payment.objects.filter(
        status='completed',
        processed_at__date=today
    )
    
    revenue_today = payments_today.aggregate(total=Sum('amount'))['total'] or 0
    payments_count_today = payments_today.count()
    
    # Monthly statistics
    current_month = timezone.now().replace(day=1)
    monthly_payments = Payment.objects.filter(
        status='completed',
        processed_at__gte=current_month
    )
    
    monthly_revenue = monthly_payments.aggregate(total=Sum('amount'))['total'] or 0
    monthly_count = monthly_payments.count()
    
    # Pending and overdue fees
    pending_fees = StudentFee.objects.filter(status='pending')
    overdue_fees = StudentFee.objects.filter(status='overdue')
    
    # Fee collection statistics
    total_pending_amount = StudentFee.objects.filter(
        status__in=['pending', 'overdue', 'partial']
    ).aggregate(
        total=Sum('total_amount') - Sum('amount_paid')
    )['total'] or 0
    
    # Recent transactions
    recent_payments = Payment.objects.filter(status='completed').order_by('-processed_at')[:15]
    
    # Payment mode distribution
    payment_modes = Payment.objects.filter(status='completed').values('payment_mode').annotate(
        count=Count('id'),
        total=Sum('amount')
    )
    
    context = {
        'revenue_today': revenue_today,
        'payments_count_today': payments_count_today,
        'monthly_revenue': monthly_revenue,
        'monthly_count': monthly_count,
        'pending_fees_count': pending_fees.count(),
        'overdue_fees_count': overdue_fees.count(),
        'total_pending_amount': total_pending_amount,
        'recent_payments': recent_payments,
        'payment_modes': payment_modes,
        'title': 'Finance Dashboard'
    }
    return render(request, 'dashboard/finance.html', context)

@login_required
def student_dashboard(request):
    """Student dashboard with personal fee and payment information"""
    if not request.user.is_student():
        return redirect('dashboard:home')
    
    try:
        student = request.user.student
    except Student.DoesNotExist:
        return redirect('accounts:student_profile')
    
    # Student's fees
    student_fees = StudentFee.objects.filter(student=student)
    
    # Fee statistics
    total_fees = student_fees.count()
    pending_fees = student_fees.filter(status__in=['pending', 'overdue']).count()
    paid_fees = student_fees.filter(status='paid').count()
    
    # Amount statistics
    total_amount = student_fees.aggregate(total=Sum('total_amount'))['total'] or 0
    paid_amount = student_fees.aggregate(total=Sum('amount_paid'))['total'] or 0
    pending_amount = total_amount - paid_amount
    
    # Overdue fees
    overdue_fees = student_fees.filter(
        due_date__lt=timezone.now().date(),
        status__in=['pending', 'overdue']
    )
    
    # Recent payments
    recent_payments = Payment.objects.filter(
        student_fee__student=student,
        status='completed'
    ).order_by('-processed_at')[:10]
    
    # Upcoming due dates
    upcoming_dues = student_fees.filter(
        due_date__gte=timezone.now().date(),
        status__in=['pending', 'partial']
    ).order_by('due_date')[:5]
    
    context = {
        'student': student,
        'total_fees': total_fees,
        'pending_fees': pending_fees,
        'paid_fees': paid_fees,
        'total_amount': total_amount,
        'paid_amount': paid_amount,
        'pending_amount': pending_amount,
        'overdue_fees': overdue_fees,
        'recent_payments': recent_payments,
        'upcoming_dues': upcoming_dues,
        'title': 'Student Dashboard'
    }
    return render(request, 'dashboard/student.html', context)
