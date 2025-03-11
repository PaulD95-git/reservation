from django.contrib import admin
from .models import Table, Reservation

# Register your models here.

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'guests', 'table', 'booking_code', 'created_at')
    search_fields = ('name', 'email', 'phone', 'booking_code')
    list_filter = ('date', 'time')
