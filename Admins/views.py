from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from Users.models import IDApplication
from .models import AdminProfile
from .forms import AdminSignUpForm, AdminLoginForm
import random  # Needed for generating the ID


def is_admin(user):
    return user.is_authenticated and user.is_staff


# --- Helper: ID Generation Logic ---
def generate_unique_id():
    """Generates a random unique 8-digit National ID number."""
    while True:
        # Generate random 8 digit number
        new_id = str(random.randint(10000000, 99999999))
        # Ensure it doesn't already exist in the database
        if not IDApplication.objects.filter(generated_id_number=new_id).exists():
            return new_id


# --- Authentication Views (Admins) ---

def admin_signin(request):
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                form.add_error(None, "Access Denied: You do not have administrative privileges.")
    else:
        form = AdminLoginForm()

    return render(request, 'Admins/signin.html', {'form': form})


def admin_signup(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect('admin_dashboard')
    else:
        form = AdminSignUpForm()

    return render(request, 'Admins/signup.html', {'form': form})


def admin_signout(request):
    logout(request)
    return redirect('admin_signin')


# --- Dashboard View (Admins) ---

@user_passes_test(is_admin, login_url='admin_signin')
def admin_dashboard(request):
    try:
        admin_profile = AdminProfile.objects.get(user=request.user)
    except AdminProfile.DoesNotExist:
        admin_profile = None

    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        action = request.POST.get('action')

        if application_id and action in ['approve', 'decline']:
            try:
                application = IDApplication.objects.get(pk=application_id)

                if action == 'approve':
                    application.status = 'APPROVED'

                    # --- ID GENERATION LOGIC ---
                    # Only generate if it's a NEW application and doesn't have one yet
                    if application.application_type == 'NEW' and not application.generated_id_number:
                        application.generated_id_number = generate_unique_id()

                elif action == 'decline':
                    application.status = 'DECLINED'

                application.save()
                return redirect('admin_dashboard')
            except IDApplication.DoesNotExist:
                pass

    applications = IDApplication.objects.all().select_related('applicant').order_by('-date_submitted')

    context = {
        'admin_name': request.user.username,
        'admin_role': admin_profile.role if admin_profile else "N/A",
        'admin_department': admin_profile.department if admin_profile else "N/A",
        'pending_count': applications.filter(status='PENDING').count(),
        'applications': applications,
    }
    return render(request, 'Admins/dashboard.html', context)