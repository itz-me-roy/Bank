# Bank App

A simple banking application built with Django. Users can sign up, log in, view
their account balance, deposit and withdraw funds, transfer money to other
accounts by account number, and view a full transaction history.

## Features

- User signup/login/logout (Django auth)
- Each user automatically gets a bank `Account` with a unique 10-digit account number
- Deposit / Withdraw funds
- Transfer funds to another user's account
- Full transaction ledger with running balance
- Django admin for managing accounts and transactions

## Project layout

```
bank_app/
├── manage.py
├── requirements.txt
├── bank_app/          # project settings, urls
└── banking/           # the banking app (models, views, templates)
    ├── models.py       # Account, Transaction
    ├── views.py
    ├── forms.py
    ├── urls.py
    ├── admin.py
    ├── migrations/
    └── templates/
```

## Setup

1. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (optional, for /admin/)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. Visit `http://127.0.0.1:8000/` to sign up and start banking, or
   `http://127.0.0.1:8000/admin/` to manage data as a superuser.

## Notes for production use

This is a learning/starter project. Before deploying it for real:

- Move `SECRET_KEY` out of `settings.py` into an environment variable.
- Set `DEBUG = False` and configure `ALLOWED_HOSTS`.
- Switch from SQLite to a production database (e.g. PostgreSQL).
- Add rate limiting / stronger validation around money-movement endpoints.
- Add HTTPS, and consider two-factor authentication for login.
- Wrap balance updates in `transaction.atomic()` and use `select_for_update()`
  to make concurrent transfers safe.
