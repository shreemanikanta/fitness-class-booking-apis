from django.db import models
from django.utils import timezone
import uuid

# Create your models here.
class FitnessClass(models.Model):
    """
    Model representing a fitness class session.

    Attributes:
        uuid (UUID): Unique identifier for the class.
        name (str): Type of fitness class (e.g., Yoga, Zumba, HIIT).
        instructor (str): Name of the instructor.
        scheduled_time (datetime): Scheduled time of the class.
        total_slots (int): Total number of slots available for booking.
        available_slots (int): Number of slots currently available.
    """
    CLASS_TYPES = (
        ('Yoga', 'Yoga'),
        ('Zumba', 'Zumba'),
        ('HIIT', 'HIIT'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, choices=CLASS_TYPES)
    instructor = models.CharField(max_length=100)
    scheduled_time = models.DateTimeField()
    total_slots = models.PositiveIntegerField()
    available_slots = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} with {self.instructor} at {self.scheduled_time}"
    
class Booking(models.Model):
    """
    Model representing a booking made by a client for a fitness class.

    Attributes:
        uuid (UUID): Unique identifier for the booking.
        fitness_class (FitnessClass): Reference to the booked fitness class.
        client_name (str): Name of the client.
        client_email (str): Email address of the client.
        booked_at (datetime): Timestamp when the booking was made.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name="bookings")
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booked_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.client_name} - {self.fitness_class.name} ({self.client_email})"