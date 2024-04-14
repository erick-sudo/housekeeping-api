from django.urls import path
from rest_framework.generics import ListAPIView
from .serializers.cleaning_frequency_serializers import CleaningFrequencySerializer
from .serializers.clean_type_serializers import CleanTypeSerializer
from .views.cleaner_views import RetrieveCleanerView
from .views.booking_views import RetrieveBookingView, CreateBookingView, AcknowledgeBookingView, UserBookingsView
from .views.credit_card_views import RetrieveCreditCardView, CreateCreditCardView
from .serializers.booking_serializers import PaymentMethodSerializer
from .models import CleaningFrequency, CleanType, PaymentMethod

urlpatterns = [
    
    path('credit_cards/retrieve', RetrieveCreditCardView.as_view(), name='retrieve_credit_card'),
    path('credit_cards/create', CreateCreditCardView.as_view(), name='create_credit_card'),
    
    path('payment_methods/list', ListAPIView.as_view(queryset=PaymentMethod.objects.all(), serializer_class=PaymentMethodSerializer), name='list_payment'),
    
    path('cleaning_frequencies', ListAPIView.as_view(queryset=CleaningFrequency.objects.all(), serializer_class=CleaningFrequencySerializer), name="cleaning_frequencies"),
    
    path('bookings/all', UserBookingsView.as_view(), name='index_booking'),
    path('bookings/<int:id>/retrieve', RetrieveBookingView.as_view(), name='retrieve_booking'),
    path('bookings/acknowledge', AcknowledgeBookingView.as_view(), name='acknowledge_booking'),
    path('bookings/create', CreateBookingView.as_view(), name='create_booking'),
    
    path('cleaners/<int:id>/retrieve', RetrieveCleanerView.as_view(), name='retrieve_cleaner'),
    path('clean_types/all', ListAPIView.as_view(queryset=CleanType.objects.all(), serializer_class=CleanTypeSerializer), name='delete_clean_type')
]