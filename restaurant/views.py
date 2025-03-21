from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm, SignupForm
from .models import Reservation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# Home view


def home(request):
    return render(request, "home.html")


# Booking view (for logged-in users)
@login_required
def book_table(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("booking_success")  # Redirect to booking success
    else:
        form = ReservationForm()
    return render(request, "reservation_form.html", {"form": form})


# Booking success view
@login_required
def booking_success(request):
    try:
        reservation = Reservation.objects.latest('created_at')  # Fetch the latest booking
    except Reservation.DoesNotExist:
        reservation = None  # No reservations exist
    return render(request, "booking_success.html", {"reservation": reservation})


# Edit booking view (only for users who created the reservation)

def edit_booking(request, booking_code):
    reservation = get_object_or_404(Reservation, booking_code=booking_code)
    print(f"Reservation for: {reservation.user}, Logged-in user: {request.user}")

    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, "Reservation updated successfully.")
            return redirect("manage_reservations")
    else:
        form = ReservationForm(instance=reservation)

    return render(request, "edit_booking.html", {"form": form, "reservation": reservation})





# Cancel booking view (only for users who created the reservation)


from django.http import JsonResponse


def cancel_booking(request, booking_code):
    reservation = get_object_or_404(Reservation, booking_code=booking_code)

    # Cancel the reservation (e.g., delete it or set status to canceled)
    reservation.delete()

    # Return a success response
    return JsonResponse({'success': True})




# User signup view
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose a different one.")
                return redirect('signup')
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to login page after signup
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


# Manage reservations for logged-in users
@login_required
def manage_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'manage_reservations.html', {'reservations': reservations})


# View to handle adding a new reservation (logged-in users only)
@login_required
def add_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_reservations')  # Redirect to manage reservations page
    else:
        form = ReservationForm()
    return render(request, 'restaurant/add_reservation.html', {'form': form})


# Make a reservation
@login_required
def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the reservation to the database
            return redirect('success')  # Redirect to a success page after reservation
    else:
        form = ReservationForm()  # Create a blank form for GET request

    return render(request, 'restaurant/reservation_form.html', {'form': form})


def menu(request):
    return render(request, 'menu.html')
