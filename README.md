E-Citizen ID Application Prototype

A Django-based platform for an online National ID application system. This project simulates the end-to-end process of applying for new or replacement IDs, featuring secure role-based authentication, automated ID number generation, and real-time M-Pesa payment integration using the Daraja API.

🚀 Key Features

👤 User Portal

Secure Authentication: User registration and login with session management.

New ID Application: * First-time applicants submit details (Place of birth, parents' details, etc.).

Logic Enforcement: Users are strictly limited to one New ID application.

Replacement ID Application: * Form to replace lost/damaged IDs.

Logic Enforcement: Users cannot apply for a replacement unless they have an existing approved ID.

Validation: The entered "Old ID Number" must match system records.

M-Pesa Integration: * STK Push: Automated payment prompt sent to the user's phone for replacement fees (KES 100).

AJAX Workflow: Smooth, non-blocking payment popup modal.

Dashboard: View application history, current status, and the assigned National ID Number.

👮 Admin Portal

Staff Authentication: Distinct registration flow creating AdminProfile with roles (e.g., Reviewer, Senior Approver).

Application Review: View detailed applicant data and uploaded documents.

Approval Workflow: * Approve: Automatically generates and assigns a unique 8-digit National ID Number to new applicants.

Decline: Updates status and informs the user.

Dashboard: Quick overview of pending tasks and recent activities.

🛠️ Tech Stack

Backend: Django 4.2 (LTS) - Chosen for compatibility with XAMPP/MariaDB.

Frontend: HTML5, Bootstrap 5 (Cards, Responsive Layouts, Modals).

Database: MySQL (via XAMPP).

Payment Gateway: Safaricom Daraja API (STK Push).

Security: Environment variables (python-dotenv) for sensitive keys.

📂 Project Structure

E-citizenID-prototype/
├── config/             # Settings (DB, Auth, M-Pesa keys) & URLs
├── Users/              # Citizen logic (Forms, Views, M-Pesa Utility)
│   ├── mpesa.py        # Daraja API integration logic
│   ├── models.py       # IDApplication model with payment fields
│   └── templates/      # User dashboard & auth pages
├── Admins/             # Staff logic
│   ├── models.py       # AdminProfile model
│   └── templates/      # Admin dashboard
├── media/              # Uploaded Passport Photos & Police Abstracts (Ignored by Git)
├── .env                # Environment variables (Ignored by Git)
└── manage.py           # Django entry point


⚙️ Installation & Setup

1. Prerequisites

Python 3.10+

XAMPP (or any MySQL Server) installed and running.

2. Clone & Environment

git clone [https://github.com/your-username/E-citizenID-prototype.git](https://github.com/your-username/E-citizenID-prototype.git)
cd E-citizenID-prototype

# Create Virtual Environment
python -m venv venv

# Activate: 
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate


3. Install Dependencies

pip install -r requirements.txt
# OR manually:
pip install "django<5.0" mysqlclient requests python-dotenv pillow


Note: We use Django < 5.0 because XAMPP usually ships with MariaDB versions older than 10.5.

4. Database Setup (MySQL)

Open XAMPP Control Panel and start Apache and MySQL.

Go to http://localhost/phpmyadmin.

Create a new database named: ecitizen_db.

Select Collation: utf8mb4_unicode_ci.

5. Environment Variables (CRITICAL)

Create a file named .env in the root directory (next to manage.py) and add your configuration:

# .env file content

# Django Security
SECRET_KEY=your_secure_random_string
DEBUG=True

# MySQL Database (XAMPP Defaults)
DB_NAME=ecitizen_db
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306

# M-Pesa Credentials (Daraja Sandbox)
MPESA_CONSUMER_KEY=your_daraja_consumer_key
MPESA_CONSUMER_SECRET=your_daraja_consumer_secret
MPESA_PASSKEY=bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919


6. Run Migrations & Create Admin

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser


7. Run Server

python manage.py runserver


Access the app at http://127.0.0.1:8000/.

📖 Usage Workflow

Register: Sign up as a Citizen at /signup/.

Apply: Submit a "New ID Application".

Approve (Admin): * Log in at /admins/signin/.

Click Approve. The system generates a unique National ID.

Check ID (User): Refresh the User Dashboard to see your assigned ID number.

Replace ID:

Go to "Replacement ID" tab.

Enter your generated ID number and M-Pesa phone number.

Click Pay & Submit.

Check your phone for the STK Push simulation.

Click "I have Paid" on the modal to finish.

🛡️ License

This project is a prototype for educational purposes.