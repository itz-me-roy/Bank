from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages

from .forms import SignUpForm, DepositForm, WithdrawForm, TransferForm
from .models import Account

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Account.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                account_type=form.cleaned_data['account_type'],
            )
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

class BankLoginView(LoginView):
    template_name = 'login.html'
class BankLogoutView(LogoutView):
    next_page = 'login'

# @login_required
# def profile_view(request):
#     account = get_object_or_404(Account, user=request.user)
#     return render(request, 'bank/profile.html', {'account': account})

# @login_required
# def edit_profile_view(request):
#     account = get_object_or_404(Account, user=request.user)
#     if request.method == 'POST':
#         form = SignUpForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             account.phone = form.cleaned_data['phone']
#             account.account_type = form.cleaned_data['account_type']
#             account.save()
#             messages.success(request, 'Profile updated successfully.')
#             return redirect('profile')
#     else:
#         form = SignUpForm(instance=request.user, initial={
#             'phone': account.phone,
#             'account_type': account.account_type,
#         })
#     return render(request, 'bank/edit_profile.html', {'form': form , 'account': account})

# @login_required
# def change_password_view(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('profile')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'bank/change_password.html', {'form': form})

@login_required
def transactions_view(request):
    account = get_object_or_404(Account, user=request.user)
    transactions = account.transactions.all().order_by('-timestamp')
    return render(request, 'transactions.html', {'transactions': transactions, 'account': account})

@login_required
def dashboard_view(request):
    account = get_object_or_404(Account, user=request.user)
    return render(request, 'dashboard.html', {'account': account, 'transactions': account.transactions.all()})

@login_required
def deposit_view(request): 
    account = get_object_or_404(Account, user=request.user)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            account.deposit(form.cleaned_data['amount'], form.cleaned_data['description'] or 'Deposit')
            messages.success(request, f'Deposited ${form.cleaned_data["amount"]} successfully.')
            return redirect('dashboard')
    else:
        form = DepositForm()
    return render(request, 'deposit.html', {'form': form, 'account': account})
@login_required
def withdraw_view(request):
    account = get_object_or_404(Account, user=request.user)
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
                try:
                    account.withdraw(form.cleaned_data['amount'], form.cleaned_data['description'] or 'Withdrawal')
                    messages.success(request, f'Withdrew ${form.cleaned_data["amount"]} successfully.')
                    return redirect('dashboard')
                except ValueError as e:
                    form.add_error(None, str(e))
    else:
        form = WithdrawForm()
    return render(request, 'withdraw.html', {'form': form, 'account': account})
@login_required
def transfer_view(request): 
    account = get_object_or_404(Account, user=request.user)
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_account = form.cleaned_data['account_number']
            if recipient_account == account.account_number:
                form.add_error('account_number', 'You cannot transfer to your own account.')
            else:
                try:
                    recipient=Account.objects.get(account_number=recipient_account)
                    account.transfer_to(recipient, form.cleaned_data['amount'], form.cleaned_data['description'] or 'Transfer')
                    messages.success(request, f'Transferred ${form.cleaned_data["amount"]} to {recipient_account.user.username} successfully.')
                    return redirect('dashboard')
                except Account.DoesNotExist:
                    form.add_error('account_number', 'Recipient account does not exist.')
                except ValueError as e:
                    form.add_error(None, str(e))
    else:
        form = TransferForm()
    return render(request, 'transfer.html', {'form': form, 'account': account})
