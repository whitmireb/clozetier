from django.urls import path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('upload/', views.index, name='uploadPage'),
    path("save_item", views.save_item, name="save_item"),
    path('outfit-creator/', views.outfit_creator_view, name='outfitCreator'),
    path('', views.index, name='index'),
    path('create/', views.select_clothing, name='AIRecommendation'),
    path('get_clothing_recommendations/', views.get_clothing_recommendations, name='get_clothing_recommendations'),
    path('recommendations/', views.show_recommendations, name='show_recommendations'),
]