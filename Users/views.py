from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json
from .forms import NewApplicantForm, ReplacementIDForm
from .models import IDApplication
from .auth_forms import CustomUserCreationForm, CustomAuthenticationForm
from .mpesa import trigger_stk_push, generate_simulated_transaction_code


# --- Authentication Views (Users) ---

def user_signin(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'Users/signin.html', {'form': form})


def user_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'Users/signup.html', {'form': form})


def user_signout(request):
    logout(request)
    return redirect('user_signin')


# --- NEW: AJAX Payment Endpoint ---
def initiate_payment(request):
    """
    API view called by JavaScript to trigger M-Pesa STK Push.
    Returns JSON to the frontend so it can show the Modal.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone_number = data.get('phone_number')
            amount = 1.00  # Keep 1.00 for testing

            if not phone_number:
                return JsonResponse({'success': False, 'message': 'Phone number required'})

            # Trigger STK Push
            success, msg, req_id = trigger_stk_push(phone_number, amount)

            if success:
                # In a real app, we'd wait for callback. Here, we send back a mock code
                # so the frontend can attach it to the final form submission.
                mock_code = generate_simulated_transaction_code()
                return JsonResponse({
                    'success': True,
                    'message': msg,
                    'transaction_code': mock_code
                })
            else:
                return JsonResponse({'success': False, 'message': msg})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


# --- Dashboard View (Updated) ---

def user_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('user_signin')

    current_user = request.user

    # Check Logic
    new_app_exists = IDApplication.objects.filter(applicant=current_user, application_type='NEW').exists()

    valid_id_record = IDApplication.objects.filter(
        applicant=current_user,
        application_type='NEW',
        status__in=['APPROVED', 'COLLECTED']
    ).first()
    has_valid_id = valid_id_record is not None

    if request.method == 'POST':
        if 'new_submit' in request.POST:
            form_type = 'NEW'
            form = NewApplicantForm(request.POST, request.FILES)
        elif 'replace_submit' in request.POST:
            form_type = 'REPLACEMENT'
            form = ReplacementIDForm(request.POST, request.FILES)
        else:
            form_type = None
            form = None

        if form and form.is_valid():
            if form_type == 'NEW' and new_app_exists:
                form.add_error(None, "You already have a New ID Application on file.")

            elif form_type == 'REPLACEMENT' and not has_valid_id:
                form.add_error(None, "Eligibility Error: You don't have an approved ID to replace.")

            else:
                application = form.save(commit=False)
                application.applicant = current_user
                application.application_type = form_type

                # --- UPDATED: Retrieve Payment Info from Hidden Field ---
                if form_type == 'REPLACEMENT':
                    # The JS injects the code into this field before submitting
                    transaction_code = request.POST.get('mpesa_code')

                    if transaction_code:
                        application.is_paid = True
                        application.amount_paid = 1.00
                        application.mpesa_code = transaction_code
                    else:
                        form.add_error(None, "Payment verification missing. Please try again.")
                        # Re-render to show error
                        application_history = IDApplication.objects.filter(applicant=current_user).order_by(
                            '-date_submitted')
                        context = {
                            'current_user': current_user.username,
                            'application_status': IDApplication.objects.filter(
                                applicant=current_user).last().get_status_display() if IDApplication.objects.filter(
                                applicant=current_user).exists() else 'None',
                            'application_history': application_history,
                            'new_app_exists': new_app_exists,
                            'has_valid_id': has_valid_id,
                            'new_form': NewApplicantForm(),
                            'replace_form': form,
                        }
                        return render(request, 'Users/dashboard.html', context)

                application.save()
                return redirect('user_dashboard')

    else:
        new_form = NewApplicantForm()
        replace_form = ReplacementIDForm()

    application_history = IDApplication.objects.filter(applicant=current_user).order_by('-date_submitted')

    context = {
        'current_user': current_user.username,
        'application_status': application_history.first().get_status_display() if application_history.exists() else 'No Application Submitted',
        'application_history': application_history,
        'new_app_exists': new_app_exists,
        'has_valid_id': has_valid_id,
        'new_form': new_form,
        'replace_form': replace_form,
    }
    return render(request, 'Users/dashboard.html', context)


def app_detail(request, app_id):
    if not request.user.is_authenticated:
        return redirect('user_signin')
    current_user = request.user
    application = get_object_or_404(IDApplication, pk=app_id)
    if application.applicant != current_user and not current_user.is_staff:
        return redirect('user_dashboard')
    if current_user.is_staff:
        base_template = 'Admins/base.html'
    else:
        base_template = 'Users/base.html'
    context = {'application': application, 'base_template': base_template}
    return render(request, 'Users/app_detail.html', context)