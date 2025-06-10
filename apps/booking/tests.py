from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.booking.models import FitnessClass, Booking


class BookingAPITestCase(APITestCase):
    """
    Test case for Booking API endpoints.
    """

    def setUp(self):
        """
        Set up a sample fitness class and valid payload for use in tests.
        """
        self.class1 = FitnessClass.objects.create(
            name="Yoga",
            instructor="Hemanth",
            scheduled_time=timezone.now() + timezone.timedelta(hours=2),
            total_slots=10,
            available_slots=10
        )

        self.valid_payload = {
            "fitness_class": str(self.class1.uuid),
            "client_name": "John Doe",
            "client_email": "john@example.com"
        }
        self.url = reverse('book-class')

    def test_get_fitness_classes(self):
        """
        Test retrieving the list of available fitness classes.
        """
        url = reverse('fitness-classes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)

    def test_create_booking_success(self):
        """
        Test successfully creating a booking.
        """
        url = reverse('book-class')
        response = self.client.post(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(response.data["data"]["client_email"], "john@example.com")

    def test_create_booking_missing_field(self):
        """
        Test booking creation fails when a required field is missing.
        """
        url = reverse('book-class')
        payload = self.valid_payload.copy()
        del payload['client_name']
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("client_name", response.data)

    def test_create_booking_duplicate_email(self):
        """
        Test booking creation fails when the email has already booked the class.
        """
        self.client.post(self.url, self.valid_payload, format='json')
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already booked", str(response.data["client_email"][0]).lower())

    def test_create_booking_invalid_uuid(self):
        """
        Test booking creation fails when an invalid UUID is provided.
        """
        payload = self.valid_payload.copy()
        payload["fitness_class"] = "invalid-uuid"
        response = self.client.post(reverse('book-class'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("must be a valid uuid", str(response.data).lower())

    def test_get_bookings_by_email(self):
        """
        Test retrieving bookings for a specific email.
        """
        Booking.objects.create(
            fitness_class=self.class1,
            client_name="John",
            client_email="john@example.com"
        )
        response = self.client.get(reverse('get-bookings') + "?email=john@example.com")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_bookings_without_email(self):
        """
        Test retrieving bookings fails when email parameter is missing.
        """
        response = self.client.get(reverse('get-bookings'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Email is required", response.data["error"])
