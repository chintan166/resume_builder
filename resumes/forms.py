# resume/forms.py
from django import forms
from .models import Resume,Contact
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ResumeCustomizationForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['data']  # This will hold the JSON data for customization


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    contact_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'address', 'contact_number', 'password1', 'password2']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']