from django import forms
from .models import Payment
from decimal import Decimal

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_mode']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '1'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.student_fee = kwargs.pop('student_fee', None)
        super().__init__(*args, **kwargs)
        
        if self.student_fee:
            max_amount = self.student_fee.remaining_amount
            self.fields['amount'].widget.attrs.update({
                'max': str(max_amount),
                'placeholder': f'Max: ${max_amount}'
            })
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        
        if amount <= 0:
            raise forms.ValidationError('Amount must be greater than 0.')
        
        if self.student_fee and amount > self.student_fee.remaining_amount:
            raise forms.ValidationError(
                f'Amount cannot exceed remaining fee amount of ${self.student_fee.remaining_amount}'
            )
        
        return amount

class CreditCardForm(forms.Form):
    card_number = forms.CharField(
        max_length=19, 
        widget=forms.TextInput(attrs={
            'placeholder': '1234 5678 9012 3456',
            'pattern': '[0-9\\s]{13,19}',
            'maxlength': '19'
        })
    )
    card_holder_name = forms.CharField(max_length=100)
    expiry_month = forms.ChoiceField(
        choices=[(i, f'{i:02d}') for i in range(1, 13)]
    )
    expiry_year = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(2025, 2031)]
    )
    cvv = forms.CharField(
        max_length=4,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'CVV',
            'maxlength': '4'
        })
    )
    
    def clean_card_number(self):
        card_number = self.cleaned_data['card_number'].replace(' ', '')
        if not card_number.isdigit() or len(card_number) < 13:
            raise forms.ValidationError('Please enter a valid card number.')
        return card_number

class DebitCardForm(CreditCardForm):
    pin = forms.CharField(
        max_length=6,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'PIN',
            'maxlength': '6'
        })
    )

class UPIForm(forms.Form):
    upi_id = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'yourname@upi'
        })
    )
    
    def clean_upi_id(self):
        upi_id = self.cleaned_data['upi_id']
        if '@' not in upi_id:
            raise forms.ValidationError('Please enter a valid UPI ID.')
        return upi_id

class CashPaymentForm(forms.Form):
    received_by = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Name of receiver'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional notes'})
    )

class BankTransferForm(forms.Form):
    bank_name = forms.CharField(max_length=100)
    account_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Account number'})
    )
    ifsc_code = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={'placeholder': 'IFSC Code'})
    )
    transaction_reference = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Transaction reference number'})
    )
