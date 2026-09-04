from django.contrib import admin
from.models import Account, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'user', 'phone', 'account_type', 'balance', 'created_at')
    search_fields = ('account_number', 'user__username')
    list_filter = ('account_type',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'amount', 'account', 'timestamp' ,'balance_after')
    search_fields = ('transaction_type',)
    list_filter = ('transaction_type',)
