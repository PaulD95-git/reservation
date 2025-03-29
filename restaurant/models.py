from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import uuid


# Table model to represent a dining table
class Table(models.Model):
    number = models.IntegerField(unique=True)  # Table number (should be unique)
    capacity = models.IntegerField()  # The seating capacity of the table

    def __str__(self):
        """Return a string representation of the table with number and capacity."""
        return f"Table {self.number} - {self.capacity} seats"


# Reservation model to represent a booking for a table
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Associated user (optional)
    name = models.CharField(max_length=255)  # Name of the person making the reservation
    email = models.EmailField()  # Email address of the person making the reservation
    phone = models.CharField(max_length=15)  # Phone number of the person making the reservation
    date = models.DateField()  # Date of the reservation
    time = models.TimeField()  # Time of the reservation
    guests = models.IntegerField()  # Number of guests for the reservation
    table = models.ForeignKey(Table, on_delete=models.CASCADE)  # Associated table for the reservation
    booking_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # Unique booking code (auto-generated)
    created_at = models.DateTimeField(default=now, editable=False)  # Timestamp when the reservation is created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the reservation is last updated

    class Meta:
        unique_together = ('date', 'time', 'table')  # Ensure no duplicate reservations for the same table at the same time

    def __str__(self):
        """Return a string representation of the reservation, including name, date, and time."""
        return f"Reservation for {self.name} on {self.date} at {self.time}"
