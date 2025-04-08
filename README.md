# KYC Approval App

A Django-based KYC (Know Your Customer) approval system with user and officer roles, document uploads, and email notifications. Celery is used for asynchronous task handling, and Redis serves as the message broker.

---

## Features

- User & officer authentication
- KYC form submission and status tracking
- Document upload (ID and address proof)
- Email notifications
- Asynchronous task processing with Celery

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/alphonsk162/kyc-approval-app

```
### 2. Create a Virtual Environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Configure .env File
```
SECRET_KEY=your_secret_key_here
MAIL_APP_PASSWORD=your_mail_app_password_here
```


### 5. Configure Database

By default, the project uses SQLite and works without additional setup. You can optionally configure PostgreSQL by updating the `DATABASES` section in `settings.py`.

### 6. Apply Migrations
```
python manage.py makemigrations
python manage.py migrate
```
### 7. Install and Start Redis Server

- Ubuntu: Use the following commands to install Redis:​
```
sudo apt update
sudo apt install redis
sudo systemctl start redis
```
- macOS: If you have Homebrew installed, execute:
```
brew update
brew install redis
brew services start redis
```

### 8.Start Celery Worker
In a new terminal, activate your virtual environment and run:
```
celery -A kyc_approval_app worker --loglevel=info

```

### 9.Start Django Development Server
 In another terminal, activate your virtual environment and execute:​
 ```
 python manage.py runserver
 ```

### 10. Accessing the App
Visit: http://127.0.0.1:8000/


## Project Structure 
```
├── kyc_approval_app
│   ├── db.sqlite3
│   ├── kyc_approval_app
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── asgi.py
│   │   ├── celery.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── __pycache__
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   ├── media
│   │   ├── address_proofs
│   │   └── id_proofs
│   ├── officer
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── helper_functions.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── __pycache__
│   │   ├── tasks.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── sample.env
│   ├── static
│   │   ├── edit_profile.css
│   │   ├── kyc_submission.css
│   │   ├── messages.css
│   │   ├── officer_home_page.css
│   │   ├── user_home_page.css
│   │   ├── user_login.css
│   │   ├── user_signup.css
│   │   └── view_request.css
│   ├── templates
│   │   ├── edit_profile.html
│   │   ├── edit_submission.html
│   │   ├── kyc_request_form.html
│   │   ├── kyc_status_email.html
│   │   ├── list_requests.html
│   │   ├── log_details.html
│   │   ├── log_list.html
│   │   ├── officer_home_page.html
│   │   ├── officer_login.html
│   │   ├── user_home_page.html
│   │   ├── user_login.html
│   │   ├── user_signup.html
│   │   └── view_request.html
│   └── user
│       ├── admin.py
│       ├── apps.py
│       ├── helper_functions.py
│       ├── __init__.py
│       ├── migrations
│       ├── models.py
│       ├── __pycache__
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── README.md
├── requirements.txt
└── venv
```
