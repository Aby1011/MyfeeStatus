from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from fees.models import StudentFee
from .models import Payment, PaymentReceipt
from .forms import (PaymentForm, CreditCardForm, DebitCardForm, UPIForm, 
                   CashPaymentForm, BankTransferForm)

@login_required
def payment_list(request):
    payments = Payment.objects.all()
    
    if request.user.is_student():
        try:
            payments = payments.filter(student_fee__student=request.user.student)
        except:
            return redirect('accounts:student_profile')
    
    context = {
        'payments': payments,
        'title': 'Payment History'
    }
    return render(request, 'payments/payment_list.html', context)

@login_required
def make_payment(request, fee_id):
    student_fee = get_object_or_404(StudentFee, pk=fee_id)
    
    # Only students can make payments
    if not request.user.is_student():
        messages.error(request, 'Only students can make payments.')
        return redirect('fees:list')
    
    # Check permissions - student can only pay their own fees
    if request.user.student != student_fee.student:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    
    if student_fee.status == 'paid':
        messages.info(request, 'This fee has already been paid.')
        return redirect('fees:list')
    
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST, student_fee=student_fee)
        
        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.student_fee = student_fee
            payment.save()
            
            # Redirect to payment processing based on payment mode
            return redirect('payments:process_payment', payment_id=payment.id)
    else:
        payment_form = PaymentForm(student_fee=student_fee)
    
    context = {
        'student_fee': student_fee,
        'payment_form': payment_form,
        'title': f'Pay Fee - {student_fee.fee_structure.name}'
    }
    return render(request, 'payments/make_payment.html', context)

@login_required
def process_payment(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    
    # Only students can process payments
    if not request.user.is_student():
        messages.error(request, 'Only students can process payments.')
        return redirect('payments:list')
    
    # Check permissions - student can only process their own payments
    if request.user.student != payment.student_fee.student:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    
    if payment.status != 'pending':
        messages.info(request, 'This payment has already been processed.')
        return redirect('payments:receipt', payment_id=payment.id)
    
    # Select appropriate form based on payment mode
    form_class = None
    if payment.payment_mode == 'credit_card':
        form_class = CreditCardForm
    elif payment.payment_mode == 'debit_card':
        form_class = DebitCardForm
    elif payment.payment_mode == 'upi':
        form_class = UPIForm
    elif payment.payment_mode == 'cash':
        form_class = CashPaymentForm
    elif payment.payment_mode == 'bank_transfer':
        form_class = BankTransferForm
    
    if request.method == 'POST':
        if form_class:
            form = form_class(request.POST)
            if form.is_valid():
                # Store relevant details (masked/safe data only)
                if payment.payment_mode in ['credit_card', 'debit_card']:
                    card_number = form.cleaned_data['card_number']
                    payment.masked_card_number = f"****-****-****-{card_number[-4:]}"
                    payment.card_holder_name = form.cleaned_data['card_holder_name']
                elif payment.payment_mode == 'upi':
                    payment.upi_id = form.cleaned_data['upi_id']
                elif payment.payment_mode == 'cash':
                    payment.notes = f"Received by: {form.cleaned_data['received_by']}"
                    if form.cleaned_data['notes']:
                        payment.notes += f"\\nNotes: {form.cleaned_data['notes']}"
                elif payment.payment_mode == 'bank_transfer':
                    payment.reference_number = form.cleaned_data['transaction_reference']
                    payment.notes = f"Bank: {form.cleaned_data['bank_name']}, Account: ****{form.cleaned_data['account_number'][-4:]}"
                
                # Process the payment
                success = payment.process_payment()
                
                if success:
                    # Generate receipt
                    receipt, created = PaymentReceipt.objects.get_or_create(payment=payment)
                    messages.success(request, 'Payment processed successfully!')
                    return redirect('payments:receipt', payment_id=payment.id)
                else:
                    messages.error(request, 'Payment processing failed. Please try again.')
                    return redirect('payments:make_payment', fee_id=payment.student_fee.id)
        else:
            # For cash payments without additional forms
            success = payment.process_payment()
            if success:
                receipt, created = PaymentReceipt.objects.get_or_create(payment=payment)
                messages.success(request, 'Payment processed successfully!')
                return redirect('payments:receipt', payment_id=payment.id)
            else:
                messages.error(request, 'Payment processing failed.')
                return redirect('payments:make_payment', fee_id=payment.student_fee.id)
    else:
        form = form_class() if form_class else None
    
    context = {
        'payment': payment,
        'form': form,
        'title': f'Process Payment - {payment.get_payment_mode_display()}'
    }
    return render(request, 'payments/process_payment.html', context)

@login_required
def payment_receipt(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    
    # Check permissions
    if request.user.is_student() and request.user.student != payment.student_fee.student:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    
    try:
        receipt = payment.receipt
    except PaymentReceipt.DoesNotExist:
        if payment.status == 'completed':
            receipt = PaymentReceipt.objects.create(payment=payment)
        else:
            messages.error(request, 'Receipt not available for incomplete payments.')
            return redirect('payments:list')
    
    context = {
        'payment': payment,
        'receipt': receipt,
        'title': f'Payment Receipt - {receipt.receipt_number}'
    }
    return render(request, 'payments/receipt.html', context)

@login_required
def payment_history(request):
    payments = Payment.objects.filter(status='completed')
    
    if request.user.is_student():
        try:
            payments = payments.filter(student_fee__student=request.user.student)
        except:
            return redirect('accounts:student_profile')
    
    context = {
        'payments': payments,
        'title': 'Payment History'
    }
    return render(request, 'payments/payment_history.html', context)

@login_required
def pending_payments(request):
    if not (request.user.is_admin() or request.user.is_finance_manager()):
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    
    pending_payments = Payment.objects.filter(status__in=['pending', 'processing'])
    
    context = {
        'payments': pending_payments,
        'title': 'Pending Payments'
    }
    return render(request, 'payments/pending_payments.html', context)
