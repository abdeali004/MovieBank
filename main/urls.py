from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('', views.movieSearch),
    path('home', views.home),
    path('register', views.register),
    path('login', views.loginUser),
    path('logout', views.logoutUser),
    path('UserData', views.UserData),
    path('search', views.movieSearch),
    path('movie/<str:imdbId>', views.movieDetail),
    path('movierecommender', views.movieMain),
]
