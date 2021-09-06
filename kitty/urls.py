from django.urls import path
from . import views

app_name = 'kitty'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('create/', views.create, name='create'),
    path('search/', views.search, name='search'),
]