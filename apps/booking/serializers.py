from rest_framework import serializers
from .models import Booking, FitnessClass
from .utils import convert_to_timezone
from django.utils.timezone import localtime
import pytz
from . import messages


class FitnessClassSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying fitness class details, including a localized scheduled time.
    """
    local_scheduled_time = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = ['uuid', 'name', 'instructor', 'scheduled_time', 'local_scheduled_time', 'total_slots', 'available_slots']
    
    def get_local_scheduled_time(self, obj):
        """
        Return scheduled_time localized to the timezone passed in query params,
        or ISO-formatted time if not specified or invalid.
        """
        request = self.context.get('request', None)
        if request:
            tz_param = request.query_params.get('timezone')
            if tz_param:
                try:
                    target_tz = pytz.timezone(tz_param)
                    return localtime(obj.scheduled_time, target_tz).isoformat()
                except pytz.UnknownTimeZoneError:
                    return obj.scheduled_time.isoformat()
        return obj.scheduled_time.isoformat()   

class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying booking details along with the class name.
    """
    fitness_class_name = serializers.CharField(source='fitness_class.name', read_only=True)
    class Meta:
        model = Booking
        fields = ['uuid', 'fitness_class', 'fitness_class_name', 'client_name', 'client_email', 'booked_at']


class BookingCreateSerializer(serializers.Serializer):
    """
    Serializer for validating and creating a new booking.
    """
    fitness_class = serializers.UUIDField()
    client_name = serializers.CharField(min_length=2, max_length=100)
    client_email = serializers.EmailField()

    def validate_fitness_class(self, value):
        """
        Validate that the fitness class exists for the given UUID.
        """
        try:
            fitness_class = FitnessClass.objects.get(uuid=value)
        except FitnessClass.DoesNotExist:
            raise serializers.ValidationError(messages.INVALID_CLASS_ID)

        self.context['fitness_class'] = fitness_class 
        return value

    def validate(self, data):
        """
        Validate that:
        - The user hasn't already booked the class.
        - The class has available slots.
        """
        fitness_class = self.context.get('fitness_class')
        email = data.get('client_email')

        if fitness_class and Booking.objects.filter(fitness_class=fitness_class, client_email__iexact=email).exists():
            raise serializers.ValidationError({
                "client_email": messages.ALREADY_BOOKED
            })
        
        if fitness_class.available_slots <= 0:
            raise serializers.ValidationError(messages.NO_SLOTS)

        return data

    def create(self, validated_data):
        """
        Create a new booking and decrement the available slots for the class.
        """
        fitness_class = self.context['fitness_class']
        booking = Booking.objects.create(
            fitness_class=fitness_class,
            client_name=validated_data['client_name'],
            client_email=validated_data['client_email']
        )
        fitness_class.available_slots -= 1
        fitness_class.save()
        return booking