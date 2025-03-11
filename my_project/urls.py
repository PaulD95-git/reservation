"""
URL configuration for my_project project.

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
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from restaurant import views  # Importing the views module

urlpatterns = [
   # Home page
    path('', views.home, name='home'),

    # Reservation form
    path('reserve/', views.book_table, name='book_table'),  

    # Booking success page after booking
    path('booking_success/', views.booking_success, name='booking_success'),

    # Admin panel
    path('admin/', admin.site.urls),  

    # Django auth URLs
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),  # Sign up URL
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout URL

    # Booking edit and cancel URLs
    path('edit/<uuid:booking_code>/', views.edit_booking, name='edit_booking'),
    path('cancel/<uuid:booking_code>/', views.cancel_booking, name='cancel_booking'),
]
