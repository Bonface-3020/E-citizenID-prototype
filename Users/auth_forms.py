from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

# Define common Bootstrap classes
BOOTSTRAP_CLASSES = 'form-control rounded-lg shadow-sm'


class CustomUserCreationForm(UserCreationForm):
    """A custom form for user registration (Sign Up)."""
    email = forms.EmailField(
        label="Email Address",
        required=True,
        widget=forms.EmailInput(attrs={'class': BOOTSTRAP_CLASSES, 'placeholder': 'Enter your valid email'}),
    )

    class Meta:
        model = UserCreationForm.Meta.model
        fields = ("username", "email")  # Password fields are handled by parent class automatically

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap styling to username
        self.fields['username'].widget.attrs.update(
            {'class': BOOTSTRAP_CLASSES, 'placeholder': 'Enter desired username'})

        # Apply Bootstrap styling to the password fields inherited from UserCreationForm
        # Note: The fields are named 'password1' and 'password2' by Django
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({'class': BOOTSTRAP_CLASSES, 'placeholder': 'Enter password'})
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update(
                {'class': BOOTSTRAP_CLASSES, 'placeholder': 'Confirm password'})


class CustomAuthenticationForm(AuthenticationForm):
    """A custom form for user login (Sign In)."""
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES, 'placeholder': 'Enter username'}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': BOOTSTRAP_CLASSES, 'placeholder': 'Enter password'}),
    )