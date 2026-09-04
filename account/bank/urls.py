from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.BankLoginView.as_view(), name='login'),
    path('logout/', views.BankLogoutView.as_view(), name='logout'),
    # path('profile/', views.profile_view, name='profile'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('transfer/', views.transfer_view, name='transfer'),
    path('transactions/', views.transactions_view, name='transactions'),
    # path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    # path('change_password/', views.change_password_view, name='change_password'),

]
