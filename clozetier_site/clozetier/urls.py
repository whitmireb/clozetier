from django.urls import path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('upload/', views.index, name='uploadPage'),
    path("save_item", views.save_item, name="save_item"),
    path("clozet/", views.clozet_view, name='clozet'),
    path('outfit-creator/', views.outfit_creator_view, name='outfitCreator'),  # Add this line
    path('', views.index, name='index'),  # Main index page
    path('get_item_details/<int:item_id>/', views.get_item_details, name='get_item_details'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('create/', views.select_clothing, name='AIRecommendation'),
    path('create/<int:item_id>/', views.select_clothing, name='AIRecommendation'),
    path('get_clothing_recommendations/', views.get_clothing_recommendations, name='get_clothing_recommendations'),
    path('recommendations/', views.show_recommendations, name='show_recommendations'),
    path('signup/', views.signup, name='signup'),  # Add the signup URL

]