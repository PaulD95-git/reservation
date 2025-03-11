from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm, SignupForm
from .models import Reservation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Home view


def home(request):
    return render(request, "home.html")

# Booking view


@login_required
def book_table(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("booking_success")
    else:
        form = ReservationForm()

    return render(request, "reservation_form.html", {"form": form})

# Booking success view


@login_required
def booking_success(request):
    reservation = Reservation.objects.latest('created_at')  # Fetch the latest booking
    return render(request, "booking_success.html", {"reservation": reservation})

# Edit booking view
@login_required
def edit_booking(request, booking_code):
    reservation = get_object_or_404(Reservation, booking_code=booking_code)

    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect("booking_success")
    else:
        form = ReservationForm(instance=reservation)

    return render(request, "edit_booking.html", {"form": form, "reservation": reservation})

# Cancel booking view
@login_required
def cancel_booking(request, booking_code):
    reservation = get_object_or_404(Reservation, booking_code=booking_code)

    if request.method == "POST":
        reservation.delete()
        return redirect("home")

    return render(request, "cancel_booking.html", {"reservation": reservation})

# User signup view


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to login page after signup
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})
