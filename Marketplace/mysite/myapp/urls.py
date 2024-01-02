"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from .views import index, detail, payment_success_view, payment_failed_view, create_checkout_session, create_product, product_edit, product_delete, dashboard, register, invalid, my_purchases, sales
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', index, name='index'),
    path('product/<int:id>/', detail, name='detail'),
    path('success/', payment_success_view, name='success'),
    path('failed/', payment_failed_view, name='failed'),
    path('api/checkout-session/<int:id>/',
         create_checkout_session, name='api_checkout_session'),
    path('createproduct/', create_product, name='createproduct'),
    path('productedit/<int:id>/', product_edit, name='productedit'),
    path('productdelete/<int:id>/', product_delete, name='productdelete'),
    path('dashboard', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('invalid/', invalid, name='invalid'),
    path('purchases/', my_purchases, name='purchases'),
    path('sales/', sales, name='sales'),
]
