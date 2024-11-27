# accounts/views.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm  # Added UserChangeForm import
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':  # Handle form submission
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log in the new user
            return redirect('home')  # Redirect to the homepage
    else:  # Handle GET requests to display the signup form
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
def profile(request):
    """
    View for the user profile. This view is accessible only to authenticated users.
    It renders the profile.html template.
    """
    return render(request, 'profile.html')


@login_required
def edit_profile(request):
    """
    View to edit the user's profile information. 
    Accessible only to authenticated users.
    """
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def activity_history(request):
    """
    View to show the user's activity history. 
    Accessible only to authenticated users.
    """
    # Placeholder for future implementation of activity history
    return render(request, 'activity_history.html')
