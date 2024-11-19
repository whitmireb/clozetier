# accounts/views.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


# New register view
def register(request):
    """
    View for user registration. Renders a form for new users to create an account.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    """
    View for the user profile. This view is accessible only to authenticated users.
    It renders the profile.html template.
    """
    return render(request, 'profile.html')


class CustomUserChangeForm(UserChangeForm):
    """
    Custom form for updating user information with selected fields.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')  # Limit fields to these only


@login_required
def edit_profile(request):
    """
    View to edit the user's profile information. 
    Accessible only to authenticated users.
    """
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def activity_history(request):
    """
    View to show the user's activity history. 
    Accessible only to authenticated users.
    """
    # Placeholder for future implementation of activity history
    return render(request, 'activity_history.html')
