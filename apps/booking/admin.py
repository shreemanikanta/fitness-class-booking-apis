from django.contrib import admin
from .models import Booking, FitnessClass

@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor', 'scheduled_time', 'total_slots', 'available_slots')
    search_fields = ('name', 'instructor')
    list_filter = ('scheduled_time', 'name')
