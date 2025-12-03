E-Citizen ID Application Prototype

A Django-based prototype for an online National ID application system. This platform streamlines the process of applying for new or replacement IDs, integrates M-Pesa payments, and provides a robust admin interface for application review and approval.

🚀 Key Features

👤 User Portal

Secure Authentication: User registration and login with session management.

New ID Application: * First-time applicants can submit details (Place of birth, parents' details, etc.).

Logic Enforcement: Strictly limits users to one New ID application.

Replacement ID Application: * Form to replace lost/damaged IDs.

Logic Enforcement: Users cannot apply for a replacement unless they have an existing approved ID in the system.

Validation: The entered "Old ID Number" must match the system records.

M-Pesa Integration: * STK Push: Automated payment prompt sent to the user's phone for replacement fees (KES 100).

Payment Tracking: Applications are only saved upon successful payment simulation.

Dashboard: View application history, current status, and the assigned National ID Number (once approved).

👮 Admin Portal

Staff Authentication: Distinct registration flow creating AdminProfile with roles (e.g., Reviewer, Senior Approver).

Application Review: View detailed applicant data and uploaded documents.

Approval Workflow: * Approve: Automatically generates and assigns a unique 8-digit National ID Number to new applicants.

Decline: Updates status and informs the user.

Dashboard: Quick overview of pending tasks and recent activities.

🛠️ Tech Stack

Backend: Django 5 (Python)

Frontend: HTML5, Bootstrap 5 (Cards, Responsive Layouts)

Database: SQLite (Prototype default)

Payment Gateway: Safaricom Daraja API (STK Push)

Styling: Custom "E-Citizen Green" theme with sticky footers and refined UI.

📂 Project Structure

E-citizenID-prototype/
├── config/             # Settings (Auth, M-Pesa keys) & URLs
├── Users/              # Citizen logic (Forms, Views, M-Pesa Utility)
│   ├── mpesa.py        # Daraja API integration logic
│   ├── models.py       # IDApplication model with payment fields
│   └── templates/      # User dashboard & auth pages
├── Admins/             # Staff logic
│   ├── models.py       # AdminProfile model
│   └── templates/      # Admin dashboard
├── media/              # Uploaded Passport Photos & Police Abstracts
└── manage.py           # Django entry point


⚙️ Installation & Setup

1. Clone & Environment

git clone [https://github.com/your-username/E-citizenID-prototype.git](https://github.com/your-username/E-citizenID-prototype.git)
cd E-citizenID-prototype

# Create Virtual Environment
python -m venv venv
# Activate: 
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate


2. Install Dependencies

You need django and requests (for M-Pesa).

pip install django requests pillow


3. Configure M-Pesa (Important!)

Open config/settings.py and scroll to the bottom. Add your Daraja Sandbox Credentials:

MPESA_CONSUMER_KEY = 'YOUR_SANDBOX_KEY'
MPESA_CONSUMER_SECRET = 'YOUR_SANDBOX_SECRET'
# Use standard sandbox passkey and URLs provided in settings.py


4. Database Setup

python manage.py makemigrations
python manage.py migrate


5. Run Server

python manage.py runserver


Access the app at http://127.0.0.1:8000/.

📖 Usage Workflow

Register a User: Sign up at /signup/. You are logged in automatically.

Apply for New ID: Fill the form. Status becomes PENDING.

Admin Approval: * Open /admins/signin/ (or use a different browser).

Log in as Admin.

Click Approve. The system generates a unique ID number.

User Dashboard: Refresh the User Dashboard. You will see the assigned National ID Number.

Replacement ID:

Try applying for a replacement.

Enter the exact ID number assigned in step 4.

Enter your M-Pesa number.

Check your phone for the STK prompt (Simulated or Real depending on keys).

Upon success, the application is submitted.

🛡️ License

This project is a prototype for educational purposes.