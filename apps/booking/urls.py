from django.urls import path
from .views import FitnessClassListView, BookingCreateView, BookingListView

urlpatterns = [
    path('classes/', FitnessClassListView.as_view(), name='fitness-classes'),
    path('book/', BookingCreateView.as_view(), name='book-class'),
    path('bookings/', BookingListView.as_view(), name='get-bookings'),
]