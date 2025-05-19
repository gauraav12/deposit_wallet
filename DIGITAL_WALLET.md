
# Digital Wallet System with Fraud Detection (Django REST Framework)

This project is a full-featured backend implementation of a digital wallet system. It allows users to register, manage wallets, perform transactions, and detect potentially fraudulent behavior using Django and Django REST Framework. The APIs follow REST principles and are documented using Swagger UI.

---

## Table of Contents

- Features
- Tech Stack
- Installation
- API Endpoints
- Admin & Bonus Features
- Security Measures
- Fraud Detection Logic
- Run Scheduled Tasks
- Folder Structure
- License

---

## Features

- User registration and login with secure password hashing
- JWT authentication for protected endpoints
- Wallet operations: deposit, withdraw, and transfer
- Transaction history for each user
- Fraud detection with basic rule-based checks
- Admin APIs for reporting and flag monitoring
- Swagger UI for API testing and documentation

---

## Tech Stack

- Django 4.2
- Django REST Framework
- JWT (via djangorestframework-simplejwt)
- SQLite (development)
- drf-yasg (Swagger API docs)
- APScheduler (for scheduled tasks)
- Python 3.9+

---

## Installation

```bash
git clone https://github.com/gauraav12/deposit_wallet.git
cd deposit_wallet

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

- Project URL: http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/swagger/
- Admin Panel: http://127.0.0.1:8000/admin/

---

## API Endpoints

| Feature           | Endpoint                   | Method | Auth Required | Description                       |
|------------------|----------------------------|--------|----------------|-----------------------------------|
| Register          | /api/register/             | POST   | No             | Create new user account           |
| Login             | /api/token/                | POST   | No             | Get JWT access and refresh token  |
| View wallet       | /api/wallet/               | GET    | Yes            | Retrieve wallet balance           |
| Deposit           | /api/wallet/deposit/       | POST   | Yes            | Deposit amount into wallet        |
| Withdraw          | /api/wallet/withdraw/      | POST   | Yes            | Withdraw funds                    |
| Transfer          | /api/wallet/transfer/      | POST   | Yes            | Transfer to another user          |
| Transactions      | /api/transactions/         | GET    | Yes            | View transaction history          |

---

## Admin & Bonus Features

| Feature                   | Endpoint                      | Method | Auth Required | Description                         |
|---------------------------|-------------------------------|--------|----------------|-------------------------------------|
| Flagged Transactions      | /api/admin/flagged/           | GET    | Yes (Admin)    | View suspected fraud                |
| Wallet Balance Summary    | /api/admin/summary/           | GET    | Yes (Admin)    | Total balance per user              |
| Top Users Report          | /api/admin/top-users/         | GET    | Yes (Admin)    | Top accounts by usage or balance    |

---

## Security Measures

- JWT authentication
- Protected endpoints via DRF permissions
- Passwords hashed by Django
- Sensitive files ignored via .gitignore

---

## Fraud Detection Logic

- Rapid Transfers: Flags users sending multiple transfers in <60 seconds
- Large Withdrawals: Flags withdrawals above ₹1000
- Flag Storage: Stored in DB using `is_flagged` field
- Email Alerts: Console-based email alerts triggered on detection

---

## Run Scheduled Tasks

```bash
python manage.py run_fraud_scan
```

This command scans all transactions and flags any anomalies.

---

## Folder Structure

digital_wallet/
├── wallet_project/
│   └── settings.py
├── wallet/
│   ├── views.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── management/commands/run_fraud_scan.py
├── db.sqlite3
├── requirements.txt
├── README.md
└── .gitignore


---


