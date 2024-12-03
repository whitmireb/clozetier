from django.urls import path
from .views import SignUpView, profile, edit_profile, activity_history

urlpatterns = [
    # User signup view
    path("signup/", SignUpView.as_view(), name="signup"),
    
    # Profile view (only accessible when logged in)
    path("profile/", profile, name="profile"),
    
    # Edit profile view (only accessible when logged in)
    path("profile/edit/", edit_profile, name="edit_profile"),
    
    # Activity history view (placeholder for now)
    path("profile/activity/", activity_history, name="activity_history"),
]
