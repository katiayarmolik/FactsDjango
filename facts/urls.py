from django.urls import path
from . import views

urlpatterns = [
    path('random/', views.random_fact, name='random_fact'),
    path('categories/', views.categories, name='categories'),
    path('saved/', views.saved_facts, name='saved_facts'),
    path('add/', views.add_fact, name='add_fact'),
    path('add-category/', views.add_category, name='add_category'),
] 