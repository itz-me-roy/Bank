from decimal import Decimal
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    account_type = forms.ChoiceField(choices=Account.ACCOUNT_TYPES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'account_type', 'password1', 'password2' ,'account_type')

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #         account = Account.objects.create(
    #             user=user,
    #             phone=self.cleaned_data['phone'],
    #             account_type=self.cleaned_data['account_type'],
    #             balance=Decimal('0.00')
    #         )
    #     return user

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    description = forms.CharField(max_length=255, required=False)

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    description = forms.CharField(max_length=255, required=False)

class TransferForm(forms.Form):
    # recipient_account_number = forms.CharField(max_length=10)
    account_number = forms.CharField(max_length=10 , label="Recipient Account Number")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    description = forms.CharField(max_length=255, required=False)
    