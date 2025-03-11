from django.shortcuts import render, redirect
from .forms import ReservationForm


def book_table(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("booking_success")  # Redirect after successful booking
    else:
        form = ReservationForm()
        return render(request, "reservation_form.html", {"form": form})
