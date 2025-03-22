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


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone', 'date', 'time', 'guests', 'table']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Generate the available time slots for selection
        self.fields['time'] = forms.ChoiceField(choices=self.get_time_choices(), widget=forms.Select())

    def get_time_choices(self):
        """Generate available time slots based on opening hours."""
        opening_hours = {
            (0, 1, 2, 3, 4): (9, 20),  # Mon-Fri: 09:00 - 20:00
            (5,): (9, 22),             # Sat: 09:00 - 22:00
            (6,): (10, 17),            # Sun: 10:00 - 17:00
        }

        choices = []
        for days, (open_hour, close_hour) in opening_hours.items():
            for hour in range(open_hour, close_hour):  # Exclude closing hour
                choices.append((f"{hour:02d}:00", f"{hour:02d}:00"))

        return choices

    def clean_time(self):
        """Validate selected time based on opening hours."""
        date = self.cleaned_data.get("date")
        time = self.cleaned_data.get("time")

        if not date or not time:
            return time  # Skip validation if missing data

        day_of_week = date.weekday()  # Monday = 0, Sunday = 6
        opening_hours = {
            (0, 1, 2, 3, 4): (9, 20),  # Mon-Fri: 09:00 - 20:00
            (5,): (9, 22),             # Sat: 09:00 - 22:00
            (6,): (10, 17),            # Sun: 10:00 - 17:00
        }

        valid_times = []
        for days, (open_hour, close_hour) in opening_hours.items():
            if day_of_week in days:
                valid_times = [datetime.time(hour, 0) for hour in range(open_hour, close_hour)]

        selected_time = datetime.datetime.strptime(time, "%H:%M").time()
        if selected_time not in valid_times:
            raise ValidationError(f"Invalid time selection. Please select an hourly time between {valid_times[0].strftime('%H:%M')} and {valid_times[-1].strftime('%H:%M')}.")
        
        return selected_time



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

