from django.contrib import admin
from django.urls import path, include
from .views import index, chatroom

urlpatterns = [
    path('', index, name='index'),
    path('<slug:slug>/', chatroom, name='chatroom'),
]