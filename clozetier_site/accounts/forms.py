from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Custom form to handle password change functionality.
    """
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}),
        label="Old Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        label="Confirm New Password"
    )

class EditProfileForm(forms.ModelForm):
    """
    Custom form to edit user profile details like first name, last name, and email.
    """
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        label="First Name"
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        label="Last Name"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        label="Email Address"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        # You could add any extra validation logic here if needed
        return cleaned_data
