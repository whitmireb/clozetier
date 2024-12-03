from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomPasswordChangeForm, EditProfileForm  # Import custom forms
from django.contrib.auth import update_session_auth_hash

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
    """
    View for user signup. This uses Django's built-in UserCreationForm.
    After successful signup, users are redirected to the login page.
    """
    form_class = UserCreationForm
    success_url = reverse_lazy("login")  # Redirect to login page after signup
    template_name = "registration/signup.html"


@login_required
def profile(request):
    """
    View to display the user profile page.
    Accessible only to authenticated users.
    """
    return render(request, 'profile.html')


@login_required
def edit_profile(request):
    """
    View to edit the user's profile information.
    Accessible only to authenticated users.
    """
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)  # Use the custom EditProfileForm
        password_change_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid() and password_change_form.is_valid():
            form.save()  # Save updated user data
            password_change_form.save()  # Save password change
            messages.success(request, "Your profile and password have been updated!")  # Success message
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = EditProfileForm(instance=request.user)  # Pre-fill form with current user data
        password_change_form = CustomPasswordChangeForm(user=request.user)

    # Pass both forms to the template
    return render(request, 'edit_profile.html', {'form': form, 'password_change_form': password_change_form})


@login_required
def activity_history(request):
    """
    View to display the user's activity history.
    Accessible only to authenticated users.
    Placeholder for future functionality.
    """
    return render(request, 'activity_history.html')


@login_required
def password_change(request):
    """
    View to change the user's password.
    Accessible only to authenticated users.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Important to keep the user logged in after password change
            messages.success(request, "Your password has been changed successfully!")
            return redirect('profile')  # Redirect to the profile page
    else:
        form = PasswordChangeForm(request.user)  # Pre-fill form with current user data

    return render(request, 'password_change.html', {'form': form})
