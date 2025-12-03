from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Define the constants for application status
STATUS_CHOICES = (
    ('PENDING', 'Pending Review'),
    ('APPROVED', 'Approved'),
    ('DECLINED', 'Declined'),
    ('COLLECTED', 'ID Collected'),
)

# Define the types of applications
TYPE_CHOICES = (
    ('NEW', 'New Applicant'),
    ('REPLACEMENT', 'Replacement ID'),
)


class IDApplication(models.Model):
    """
    Core model to store all ID application data (New and Replacement).
    """
    # CORE METADATA
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    application_type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='NEW')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    date_submitted = models.DateTimeField(auto_now_add=True)

    # GENERAL APPLICANT DETAILS
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    passport_picture = models.FileField(upload_to='passports/')

    # NEW APPLICANT SPECIFIC FIELDS
    county_of_birth = models.CharField(max_length=100, null=True, blank=True)
    subcounty_of_birth = models.CharField(max_length=100, null=True, blank=True)
    location_of_birth = models.CharField(max_length=100, null=True, blank=True)
    sublocation_of_birth = models.CharField(max_length=100, null=True, blank=True)
    guardian_name = models.CharField(max_length=255, null=True, blank=True)
    guardian_id_number = models.CharField(max_length=20, null=True, blank=True)
    guardian_phone = models.CharField(max_length=20, null=True, blank=True)
    death_certificate_number = models.CharField(max_length=50, null=True, blank=True)

    # REPLACEMENT ID SPECIFIC FIELDS
    old_id_number = models.CharField(max_length=20, null=True, blank=True)
    police_abstract_form = models.FileField(upload_to='abstracts/', null=True, blank=True)

    # --- PAYMENT FIELDS ---
    is_paid = models.BooleanField(default=False, help_text="True if M-Pesa payment was successful.")
    mpesa_code = models.CharField(max_length=50, null=True, blank=True, help_text="M-Pesa Transaction ID")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # --- NEW: SYSTEM GENERATED ID ---
    # This stores the unique ID number generated upon approval of a NEW application.
    generated_id_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        unique=True,
        help_text="System generated National ID Number (8 digits)"
    )

    def __str__(self):
        return f"{self.full_name} - {self.get_application_type_display()} ({self.get_status_display()})"

    class Meta:
        verbose_name = "ID Application"
        verbose_name_plural = "ID Applications"
        ordering = ['-date_submitted']