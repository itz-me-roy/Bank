import random
import string
from decimal import Decimal

from django.conf import settings
from django.db import models


def generate_account_number():
    """Generate a unique 10-digit account number."""
    while True:
        number = ''.join(random.choices(string.digits, k=10))
        if not Account.objects.filter(account_number=number).exists():
            return number


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('SAVINGS', 'Savings'),
        ('CHECKING', 'Checking'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='account'
    )
    phone = models.CharField(max_length=15)
    account_number = models.CharField(
        max_length=10, unique=True, default=generate_account_number, editable=False
    )
    account_type = models.CharField(
        max_length=10, choices=ACCOUNT_TYPES, default='SAVINGS'
    )
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.account_number}'

    def deposit(self, amount, description='Deposit'):
        amount = Decimal(amount)
        self.balance += amount
        self.save()
        Transaction.objects.create(
            account=self,
            transaction_type='DEPOSIT',
            amount=amount,
            balance_after=self.balance,
            description=description,
        )

    def withdraw(self, amount, description='Withdrawal'):
        amount = Decimal(amount)
        if amount > self.balance:
            raise ValueError('Insufficient funds')
        self.balance -= amount
        self.save()
        Transaction.objects.create(
            account=self,
            transaction_type='WITHDRAWAL',
            amount=amount,
            balance_after=self.balance,
            description=description,
        )

    def transfer_to(self, other_account, amount, description=''):
        amount = Decimal(amount)
        if amount > self.balance:
            raise ValueError('Insufficient funds')
        self.balance -= amount
        self.save()
        other_account.balance += amount
        other_account.save()

        Transaction.objects.create(
            account=self,
            transaction_type='TRANSFER_OUT',
            amount=amount,
            balance_after=self.balance,
            description=description or f'Transfer to {other_account.account_number}',
        )
        Transaction.objects.create(
            account=other_account,
            transaction_type='TRANSFER_IN',
            amount=amount,
            balance_after=other_account.balance,
            description=description or f'Transfer from {self.account_number}',
        )


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER_OUT', 'Transfer Out'),
        ('TRANSFER_IN', 'Transfer In'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.transaction_type} of {self.amount} on {self.account.account_number}'