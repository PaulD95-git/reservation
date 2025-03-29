from django import forms
from .models import Reservation
from django.core.exceptions import ValidationError
import datetime
from django.contrib.auth.models import User

# ReservationForm is the form to handle reservations
class ReservationForm(forms.ModelForm):
    # Define the time field as a ChoiceField with empty choices initially
    time = forms.ChoiceField(choices=[], widget=forms.Select())  # ✅ Define properly

    class Meta:
        model = Reservation  # Bind the form to the Reservation model
        fields = ['name', 'email', 'phone', 'date', 'time', 'guests', 'table']  # Define which fields from the model to include
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # Specify that the date field should use a date picker input
        }

    def __init__(self, *args, **kwargs):
        """Initialize the form and set time choices if a date is selected."""
        super().__init__(*args, **kwargs)

        # If a date is already selected, populate the time choices
        if 'date' in self.data:
            date = self.data.get('date')
            self.fields['time'].choices = self.get_time_choices(date)  # Call method to get time options based on the selected date
        else:
            # If no date selected, set default choice to prompt user to select a time
            self.fields['time'].choices = [("", "Select a time")]

    def get_time_choices(self, date):
        """
        Generate available time slots based on the opening hours and table availability.
        Returns a list of available times that are not already booked.
        """
        try:
            # Get the day of the week from the selected date
            day_of_week = datetime.datetime.strptime(date, "%Y-%m-%d").weekday()
        except ValueError:
            # If the date is invalid, return an empty list
            return []

        # Define opening hours for each day of the week
        opening_hours = {
            (0, 1, 2, 3, 4): (9, 20),  # Mon-Fri: 09:00 - 20:00
            (5,): (9, 22),             # Sat: 09:00 - 22:00
            (6,): (10, 17),            # Sun: 10:00 - 17:00
        }

        choices = []
        # Loop through opening hours and check if the selected day has defined opening hours
        for days, (open_hour, close_hour) in opening_hours.items():
            if day_of_week in days:
                # For each hour between open and close, check if the time is available
                for hour in range(open_hour, close_hour):
                    time_str = f"{hour:02d}:00"  # Format the hour as 'HH:00'

                    # Check if a reservation exists at this time for the selected date
                    if not Reservation.objects.filter(date=date, time=time_str).exists():
                        # If no reservation exists, add this time to the choices list
                        choices.append((time_str, time_str))

        return choices  # Return the list of available times

    def clean(self):
        """Perform additional validation to ensure the selected table is not already booked."""
        cleaned_data = super().clean()  # Get the cleaned data from the form
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")
        table = cleaned_data.get("table")

        if date and time and table:
            # Check if the selected table is already booked at the given time for the selected date
            if Reservation.objects.filter(date=date, time=time, table=table).exists():
                raise ValidationError(f"⚠️ Table {table.number} is already booked at {time} on {date}. Please select another time.")

        return cleaned_data  # Return the cleaned data after validation


# SignupForm is the form for user registration
class SignupForm(forms.ModelForm):
    # Password field with password input type
    password = forms.CharField(widget=forms.PasswordInput)

    # Password confirmation field to ensure passwords match
    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User  # Bind the form to the User model
        fields = ['username', 'email']  # Include username and email fields from the User model

    def clean_password_confirmation(self):
        """
        Validate that the password and password confirmation fields match.
        If they don't, raise a validation error.
        """
        password = self.cleaned_data.get('password')  # Get the password from cleaned data
        password_confirmation = self.cleaned_data.get('password_confirmation')  # Get the confirmation password

        # If the passwords do not match, raise an error
        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")    
        return password_confirmation  # Return the confirmation password if validation passes
