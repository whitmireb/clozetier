from django.urls import path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("save_item", views.save_item, name="save_item"),
    # path('upload/', views.image_upload, name='image_upload'),
]