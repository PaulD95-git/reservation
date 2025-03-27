from django import forms
from .models import Reservation
from django.core.exceptions import ValidationError
import datetime
from django.contrib.auth.models import User


from django import forms
from .models import Reservation
from django.core.exceptions import ValidationError
import datetime
from django.contrib.auth.models import User


from django import forms
from .models import Reservation
from django.core.exceptions import ValidationError
import datetime


class ReservationForm(forms.ModelForm):
    time = forms.ChoiceField(choices=[], widget=forms.Select())  # ✅ Define properly

    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone', 'date', 'time', 'guests', 'table']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If a date is already selected, populate the time choices
        if 'date' in self.data:
            date = self.data.get('date')
            self.fields['time'].choices = self.get_time_choices(date)
        else:
            self.fields['time'].choices = [("", "Select a time")]

    def get_time_choices(self, date):
        """Generate available time slots based on the opening hours and table availability."""
        try:
            day_of_week = datetime.datetime.strptime(date, "%Y-%m-%d").weekday()
        except ValueError:
            return []  # If date is invalid, return empty list

        opening_hours = {
            (0, 1, 2, 3, 4): (9, 20),  # Mon-Fri: 09:00 - 20:00
            (5,): (9, 22),             # Sat: 09:00 - 22:00
            (6,): (10, 17),            # Sun: 10:00 - 17:00
        }

        choices = []
        for days, (open_hour, close_hour) in opening_hours.items():
            if day_of_week in days:
                for hour in range(open_hour, close_hour):
                    time_str = f"{hour:02d}:00"
                    
                    # Check if a reservation exists at this time
                    if not Reservation.objects.filter(date=date, time=time_str).exists():
                        choices.append((time_str, time_str))

        return choices

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")
        table = cleaned_data.get("table")

        if date and time and table:
            # Check if the selected table is already booked at the given time
            if Reservation.objects.filter(date=date, time=time, table=table).exists():
                raise ValidationError(f"⚠️ Table {table.number} is already booked at {time} on {date}. Please select another time.")

        return cleaned_data



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

