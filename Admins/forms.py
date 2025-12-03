from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import AdminProfile

# Define common Bootstrap classes for consistent styling
BOOTSTRAP_CLASSES = 'form-control rounded-lg shadow-sm'


# -----------------------------
#   ADMIN ACCOUNT SIGNUP FORM
# -----------------------------
class AdminSignUpForm(forms.Form):
    """
    Custom form to handle the creation of a User AND an AdminProfile simultaneously.
    Inherits from forms.Form for flexibility.
    """
    # User Model Fields
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES, 'placeholder': 'Enter Username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': BOOTSTRAP_CLASSES, 'placeholder': 'Enter Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': BOOTSTRAP_CLASSES, 'placeholder': 'Enter Password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': BOOTSTRAP_CLASSES, 'placeholder': 'Confirm Password'})
    )

    # AdminProfile Model Fields
    role = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES, 'placeholder': 'Enter Role (e.g., Reviewer)'})
    )
    department = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES, 'placeholder': 'Enter Department'})
    )
    is_senior_reviewer = forms.BooleanField(
        required=False,
        label="Is Senior Reviewer?",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    # -------------------------
    #   CUSTOM VALIDATION
    # -------------------------
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password2")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match.")

        return cleaned_data

    # -------------------------
    #    SAVE METHOD
    # -------------------------
    def save(self):
        """
        Creates the User and the associated AdminProfile.
        """
        data = self.cleaned_data

        # 1. Create the User
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )

        # 2. Create the AdminProfile linked to the new User
        AdminProfile.objects.create(
            user=user,
            role=data['role'],
            department=data['department'],
            is_senior_reviewer=data['is_senior_reviewer']
        )

        return user


# -----------------------------
#        ADMIN LOGIN FORM
# -----------------------------
class AdminLoginForm(AuthenticationForm):
    """
    Standard Django AuthenticationForm with Bootstrap styling applied.
    """
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES, 'placeholder': 'Enter Username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': BOOTSTRAP_CLASSES, 'placeholder': 'Enter Password'})
    )