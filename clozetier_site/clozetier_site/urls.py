"""
URL configuration for clozetier project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from accounts import views  # Import views from accounts app

urlpatterns = [
    # Admin site path
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")), 
    path("accounts/", include("django.contrib.auth.urls")),
    path('clozetier/', include('clozetier.urls')),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('signup/', TemplateView.as_view(template_name='registration/signup.html'), name='signup')
]

# Serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Additional URLs for accounts app
urlpatterns += [
    path("profile/", views.profile, name="profile"),  # User profile
    path("profile/edit/", views.edit_profile, name="edit_profile"),  # Edit user profile
    path("profile/activity/", views.activity_history, name="activity_history"),  # User activity history
]
