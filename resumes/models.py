# resume/models.py
from django.db import models
from django.contrib.auth.models import User
import json

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"


class ResumeTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='templates/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # New price field

    def __str__(self):
        return self.name

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE,null=True)
    data = models.JSONField(default=dict,null=True)  # Make sure it's a JSONField to store the dictionary
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)  # ✅ Add this


    def save(self, *args, **kwargs):
        # Ensure that the 'data' field is always a dictionary (even if it's empty)
        if not isinstance(self.data, dict):
            self.data = {}
        super().save(*args, **kwargs)
    
class ResumeOrder(models.Model):
    
    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    professional_summary = models.TextField(blank=True, null=True)  # Added professional summary
    full_name = models.CharField(max_length=100, blank=True,null=True)
    email = models.CharField(max_length=100, blank=True,null=True)
    phone = models.CharField(max_length=100, blank=True,null=True)
    linkedin = models.CharField(max_length=100, blank=True,null=True)
    degree = models.CharField(max_length=100, blank=True,null=True)
    college = models.CharField(max_length=100, blank=True,null=True)
    year = models.CharField(max_length=100, blank=True,null=True)
    company_name = models.CharField(max_length=100, blank=True,null=True)
    role = models.CharField(max_length=100, blank=True,null=True)
    duration = models.CharField(max_length=100, blank=True,null=True)
    skills = models.CharField(max_length=100, blank=True,null=True)
    certifications = models.CharField(max_length=100, blank=True,null=True)
    languages = models.CharField(max_length=100, blank=True,null=True)
    interest = models.CharField(max_length=100, blank=True,null=True)
    template = models.ForeignKey(ResumeTemplate, on_delete=models.CASCADE)
    font_family = models.CharField(max_length=100, blank=True,null=True)
    font_size = models.CharField(max_length=10, blank=True,null=True)
    font_weight = models.CharField(max_length=50, blank=True,null=True)
    font_color = models.CharField(max_length=20, blank=True,null=True)
    background_color = models.CharField(max_length=20, null=True)
    font_style = models.CharField(max_length=20, blank=True,null=True)
    border_style = models.CharField(max_length=20, null=True)
    section_spacing = models.CharField(max_length=20, blank=True,null=True)
    section_alignment = models.CharField(max_length=20, blank=True,null=True)
    projects = models.JSONField(default=list, blank=True, null=True)
    education = models.JSONField(default=list, blank=True, null=True)
    pdf_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    qr_payment = models.FileField(upload_to='payments/', null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)  # Added Profile Photo
    qr_code_image = models.ImageField(upload_to='orders/qr_codes/', null=True, blank=True)
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending"
    )  # Payment status
    is_approved = models.BooleanField(default=False)  # Admin approval

    def __str__(self):
        return f"Resume Order - {self.user.username}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " - " + self.subject
