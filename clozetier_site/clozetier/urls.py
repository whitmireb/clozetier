from django.urls import path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Import views from the current app (clozetier)
from accounts import views as accounts_views  # Import views from the accounts app

urlpatterns = [
    # Clozetier URLs (for the main application)
    path('upload/', views.index, name='uploadPage'),
    path('save_item/', views.save_item, name='save_item'),
    path('clozet/', views.clozet_view, name='clozet'),
    path('outfit-creator/', views.outfit_creator_view, name='outfitCreator'),
    path('', views.index, name='index'),  # Main index page (default route)
    path('get_item_details/<int:item_id>/', views.get_item_details, name='get_item_details'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('create/', views.select_clothing, name='AIRecommendation'),
    path('create/<int:item_id>/', views.select_clothing, name='AIRecommendation'),
    path('get_clothing_recommendations/', views.get_clothing_recommendations, name='get_clothing_recommendations'),
    path('recommendations/', views.show_recommendations, name='show_recommendations'),

    # Static Pages (using TemplateView to render static pages)
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),

    # Accounts URLs (for user authentication and profile management)
    path('signup/', accounts_views.signup, name='signup'),  # Add the signup URL,  # Signup view for new users
    path('profile/', accounts_views.profile, name='profile'),  # User profile page
    path('profile/edit/', accounts_views.edit_profile, name='edit_profile'),  # Edit user profile
    path('profile/activity/', accounts_views.activity_history, name='activity_history'),  # User activity history
    path('profile/password_change/', accounts_views.password_change, name='password_change'),  # Password change page

    # Add more URLs for other pages related to user authentication if needed
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
