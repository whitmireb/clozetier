from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path('upload/', views.image_upload, name='image_upload'),
]