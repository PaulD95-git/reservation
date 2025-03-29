from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm, SignupForm
from .models import Reservation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render
import datetime
from django.http import JsonResponse


# Home view: Renders the homepage template
def home(request):
    return render(request, "home.html")


# Booking view (for logged-in users)
@login_required
def book_table(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)  # Create a form with POST data
        if form.is_valid():  # If the form is valid, save the reservation
            form.save()
            return redirect("booking_success")  # Redirect to the booking success page
    else:
        form = ReservationForm()  # If not a POST request, show a blank form
    return render(request, "reservation_form.html", {"form": form})


# Booking success view: Displays the latest reservation created
@login_required
def booking_success(request):
    try:
        reservation = Reservation.objects.latest('created_at')  # Fetch the latest booking
    except Reservation.DoesNotExist:
        reservation = None  # If no reservations exist, set reservation to None
    return render(request, "booking_success.html", {"reservation": reservation})


# Edit booking view (only for users who created the reservation)
def edit_booking(request, booking_code):
    reservation = get_object_or_404(Reservation, booking_code=booking_code)  # Fetch reservation by booking code
    print(f"Reservation for: {reservation.user}, Logged-in user: {request.user}")

    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)  # Pre-populate the form with the reservation data
        if form.is_valid():  # If the form is valid, save the updated data
            form.save()
            messages.success(request, "Reservation updated successfully.")
            return redirect("manage_reservations")  # Redirect to manage reservations page after update
    else:
        form = ReservationForm(instance=reservation)  # Display the form with current reservation data

    return render(request, "edit_booking.html", {"form": form, "reservation": reservation})


# Cancel booking view (only for users who created the reservation)
def cancel_booking(request, booking_code):
    reservation = get_object_or_404(Reservation, booking_code=booking_code)  # Get reservation by booking code

    reservation.delete()  # Cancel the reservation by deleting it from the database

    # Return a success response in JSON format
    return JsonResponse({'success': True})


# User signup view
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)  # Create the signup form with POST data
        if form.is_valid():  # If the form is valid, create the user
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():  # Check if the username already exists
                messages.error(request, "Username already exists. Please choose a different one.")
                return redirect('signup')  # Redirect back to signup page if username exists
            user = form.save(commit=False)  # Create the user but don't save yet
            user.set_password(form.cleaned_data['password'])  # Set the user's password
            user.save()  # Save the new user to the database
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = SignupForm()  # Display a blank form if not a POST request

    return render(request, 'signup.html', {'form': form})


# Manage reservations for logged-in users
@login_required
def manage_reservations(request):
    reservations = Reservation.objects.all()  # Fetch all reservations
    return render(request, 'manage_reservations.html', {'reservations': reservations})


# View to handle adding a new reservation (logged-in users only)
@login_required
def add_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)  # Create the reservation form with POST data
        if form.is_valid():  # If the form is valid, save the new reservation
            form.save()
            return redirect('manage_reservations')  # Redirect to manage reservations page
    else:
        form = ReservationForm()  # If not a POST request, show a blank form
    return render(request, 'restaurant/add_reservation.html', {'form': form})


# Make a reservation (logged-in users only)
@login_required
def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)  # Create the reservation form with POST data
        if form.is_valid():  # If the form is valid, save the reservation
            form.save()  # Save the reservation to the database
            return redirect('success')  # Redirect to a success page after reservation
    else:
        form = ReservationForm()  # Create a blank form for GET request

    return render(request, 'restaurant/reservation_form.html', {'form': form})


# Menu view: Renders the menu page
def menu(request):
    return render(request, 'menu.html')


# About view: Renders the about page
def about(request):
    return render(request, 'about.html')


# Contact view: Handles contact form submission and sends an email
def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Send an email with the contact form details
        send_mail(
            f"New Contact Message from {name}",
            message,
            email,
            ["yourrestaurant@example.com"],  # Replace with your restaurant's email
            fail_silently=False,
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")  # Redirect to the same contact page after submission

    return render(request, "contact.html")


# View to handle Google Maps API key
def your_view(request):
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')  # Get API key from environment variable
    return render(request, 'your_template.html', {'api_key': api_key})


# Reservation form view (handles reservation form submission)
def reservation_form(request):
    form = ReservationForm(request.POST or None)  # Create form with POST data or empty if GET
    if request.method == 'POST' and form.is_valid():
        form.save()  # Save the reservation if form is valid
        return render(request, 'reservation_success.html')  # Show success page

    return render(request, 'reservation_form.html', {'form': form})


# Get available times for the selected date
def get_available_times(request):
    date = request.GET.get('date')  # Get the selected date from query params
    if date:
        form = ReservationForm(data={'date': date})  # Create form with the selected date
        time_choices = form.get_time_choices(date)  # Get available time choices for the date

        # Return available times as a JSON response
        return JsonResponse({'times': [time[1] for time in time_choices]})
    return JsonResponse({'times': []})  # Return empty list if no date is selected
