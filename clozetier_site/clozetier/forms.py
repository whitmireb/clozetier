from django import forms
from .models import ClothingItem
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

class ClothingItemForm(forms.ModelForm):
    """
    Form for adding and editing clothing items.
    """

    class Meta:
        model = ClothingItem
        fields = ['image', 'cloth_type', 'cloth_color']
        widgets = {
            'cloth_type': forms.Select(attrs={'class': 'form-control'}),
            'cloth_color': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'image': 'Upload Image',
            'cloth_type': 'Clothing Type',
            'cloth_color': 'Clothing Color',
        }


class EditProfileForm(UserChangeForm):
    """
    Form for editing user profile information.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Form for changing the user password.
    This form extends Django's built-in PasswordChangeForm and customizes its appearance.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})
