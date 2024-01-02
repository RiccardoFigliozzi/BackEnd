"""
URL configuration for socialproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password_change/', auth_view.PasswordChangeView.as_view(template_name='users/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_view.PasswordChangeDoneView.as_view(template_name='users/password_change_form_done.html'), name='password_change_done'),
    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='users/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='users/password_reset_form_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_view.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done', auth_view.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('registration/', views.user_registration, name='registration'),
    path('registration/done', views.user_registration, name='registration_done'),
    path('edit/', views.edit, name='edit'),
]
