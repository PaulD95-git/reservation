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

# Import necessary modules and views
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from restaurant import views  # Importing views from the 'restaurant' app

# Define URL patterns
urlpatterns = [
    # Auth-related URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  

    # Restaurant reservation related URLs
    path('book_table/', views.book_table, name='book_table'),  
    path('booking_success/', views.booking_success, name='booking_success'),  

    # Booking management URLs
    path('edit_booking/<uuid:booking_code>/', views.edit_booking, name='edit_booking'),  
    path('cancel_booking/<uuid:booking_code>/', views.cancel_booking, name='cancel_booking'),  

    # Sign up and manage reservations URLs
    path('signup/', views.signup, name='signup'),  
    path('manage_reservations/', views.manage_reservations, name='manage_reservations'),  

    # Other restaurant-related URLs
    path('add_reservation/', views.add_reservation, name='add_reservation'),  
    path('make_reservation/', views.make_reservation, name='make_reservation'),  
    path('menu/', views.menu, name='menu'),  
    path('about/', views.about, name='about'),

    # Correct the contact path here:
    path('contact/', views.contact_view, name='contact'),
    path('get-available-times/', views.get_available_times, name='get_available_times'),

    # Home page
    path('', views.home, name='home'),  

    # Admin
    path('admin/', admin.site.urls),

]
