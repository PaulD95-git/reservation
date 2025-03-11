from django import forms
from .models import Reservation
from django.core.exceptions import ValidationError
import datetime
from django.contrib.auth.models import User


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone', 'date', 'time', 'guests', 'table']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_time(self):
        date = self.cleaned_data.get("date")
        time = self.cleaned_data.get("time")

        if not date or not time:
            return time  # Skip validation if missing data

        day_of_week = date.weekday()  # Monday = 0, Sunday = 6
        opening_hours = {
            (0, 1, 2, 3, 4): (datetime.time(9, 0), datetime.time(20, 0)),  # Mon-Fri: 09:00 - 20:00
            (5,): (datetime.time(9, 0), datetime.time(22, 0)),             # Sat: 09:00 - 22:00
            (6,): (datetime.time(10, 0), datetime.time(17, 0)),            # Sun: 10:00 - 17:00
        }

        for days, (open_time, close_time) in opening_hours.items():
            if day_of_week in days:
                if not (open_time <= time <= close_time):
                    raise ValidationError(f"Reservations can only be made between {open_time.strftime('%H:%M')} and {close_time.strftime('%H:%M')} on this day.")        
        return time


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")
        return password_confirmation
