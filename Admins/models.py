from django.db import models
from django.contrib.auth.models import User


class AdminProfile(models.Model):
    """
    Extends the built-in Django User model to add administrative-specific fields.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=100,
        default='Reviewer',
        help_text="The administrative role (e.g., Senior Approver, Data Entry)."
    )
    department = models.CharField(
        max_length=100,
        default='National Registration',
        help_text="The department the administrator belongs to."
    )
    is_senior_reviewer = models.BooleanField(
        default=False,
        help_text="Designates if this admin can finalize application approval/rejection."
    )

    def __str__(self):
        return f"Admin Profile for {self.user.username}"

    class Meta:
        verbose_name = "Administrator Profile"
        verbose_name_plural = "Administrator Profiles"