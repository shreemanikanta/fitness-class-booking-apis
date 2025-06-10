from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Booking, FitnessClass
from .serializers import BookingSerializer, FitnessClassSerializer, BookingCreateSerializer
from rest_framework.views import APIView
from .messages import EMAIL_REQUIRED, FETCH_SUCCESS, BOOK_SUCCESS


class FitnessClassListView(APIView):
    """
    API view to retrieve a list of upcoming fitness classes.
    """

    def get(self, request):
        """
        Returns a list of all fitness classes scheduled for the future.
        """
        now = timezone.now()
        classes = FitnessClass.objects.filter(scheduled_time__gte=now).order_by('scheduled_time')
        serializer = FitnessClassSerializer(classes, many=True, context={'request': request})
        return Response({"message": FETCH_SUCCESS, "data": serializer.data}, status=status.HTTP_200_OK)
    
class BookingCreateView(APIView):
    """
    API view to create a new booking for a fitness class.
    """

    def post(self, request):
        """
        Creates a booking if the submitted data is valid.
        """
        serializer = BookingCreateSerializer(data=request.data, context={})
        if serializer.is_valid():
            booking = serializer.save()
            response_data = BookingSerializer(booking).data
            return Response({
                "message": BOOK_SUCCESS,
                "data": response_data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingListView(APIView):
    """
    API view to retrieve bookings based on the client's email.
    """

    def get(self, request):
        """
        Returns a list of bookings for the given email address.
        If no email is provided, returns a 400 error.
        """
        email = request.query_params.get('email')
        if not email:
            return Response({ "error": EMAIL_REQUIRED }, status=status.HTTP_400_BAD_REQUEST)

        bookings = Booking.objects.filter(client_email=email).order_by('-booked_at')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
