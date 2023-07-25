from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_menu, name='main_menu'),
    path('random_song/', views.random_song, name='random_song'),
    path('increase_score/<str:team>/', views.increase_score, name='increase_score'),
    path('reset_score/', views.reset_score, name='reset_score'),
]
