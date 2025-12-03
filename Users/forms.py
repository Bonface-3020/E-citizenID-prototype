from django import forms
from .models import IDApplication

# Common Bootstrap styling
BOOTSTRAP_CLASSES = 'form-control rounded-lg shadow-sm'
FILE_CLASSES = 'form-control-file rounded-lg'


class NewApplicantForm(forms.ModelForm):
    """
    Form for first-time ID applicants.
    """

    class Meta:
        model = IDApplication
        fields = [
            'full_name', 'phone_number', 'email', 'passport_picture',
            'county_of_birth', 'subcounty_of_birth', 'location_of_birth', 'sublocation_of_birth',
            'guardian_name', 'guardian_id_number', 'guardian_phone', 'death_certificate_number'
        ]

        widgets = {
            'application_type': forms.HiddenInput(attrs={'value': 'NEW'}),
            'full_name': forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES}),
            'phone_number': forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES}),
            'email': forms.EmailInput(attrs={'class': BOOTSTRAP_CLASSES}),
            'passport_picture': forms.ClearableFileInput(attrs={'class': FILE_CLASSES}),
            'county_of_birth': forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES}),
            'subcounty_of_birth': forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES}),
            'location_of_birth': forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES}),
            'sublocation_of_birth': forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES}),
            'guardian_name': forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES}),
            'guardian_id_number': forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES}),
            'guardian_phone': forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES}),
            'death_certificate_number': forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.initial.get('application_type'):
            self.initial['application_type'] = 'NEW'


class ReplacementIDForm(forms.ModelForm):
    """
    Form for replacing a lost or damaged ID.
    Includes M-Pesa Payment Field.
    """
    # Extra field for M-Pesa number (handled in view, not saved directly to this model field)
    mpesa_payment_number = forms.CharField(
        label="M-Pesa Phone Number",
        max_length=15,
        required=True,
        help_text="Format: 07XXXXXXXX or 2547XXXXXXXX",
        widget=forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES, 'placeholder': 'e.g., 0712345678'})
    )

    class Meta:
        model = IDApplication
        fields = [
            'full_name', 'phone_number', 'email', 'passport_picture',
            'old_id_number', 'police_abstract_form'
        ]

        widgets = {
            'application_type': forms.HiddenInput(attrs={'value': 'REPLACEMENT'}),
            'full_name': forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES}),
            'phone_number': forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES}),
            'email': forms.EmailInput(attrs={'class': BOOTSTRAP_CLASSES}),
            'passport_picture': forms.ClearableFileInput(attrs={'class': FILE_CLASSES}),
            'old_id_number': forms.TextInput(attrs={'class': BOOTSTRAP_CLASSES}),
            'police_abstract_form': forms.ClearableFileInput(attrs={'class': FILE_CLASSES}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.initial.get('application_type'):
            self.initial['application_type'] = 'REPLACEMENT'