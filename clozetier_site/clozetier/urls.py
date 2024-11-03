from django.urls import path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('upload/', views.index, name='uploadPage'),
    path('outfit-creator/', views.outfit_creator_view, name='outfitCreator'),  # Add this line
    path('', views.index, name='index'),  # Main index page
    # path('upload/', views.image_upload, name='image_upload'),
]