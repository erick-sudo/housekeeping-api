from django.urls import path
from rest_framework.generics import ListAPIView
from .views.cleaner_views import RetrieveCleanerView, CreateCleanerView, DestroyCleanerView
from .views.booking_views import RetrieveBookingView, CreateBookingView, AcknowledgeBookingView
from .views.clean_type_views import RetrieveCleanTypeView, CreateCleanTypeView, DestroyCleanTypeView
from .views.credit_card_views import RetrieveCreditCardView, CreateCreditCardView, DestroyCreditCardView
from .serializers.booking_serializers import BookingSerializer
from .models import Booking

urlpatterns = [
    
    path('credit_cards/retrieve', RetrieveCreditCardView.as_view(), name='retrieve_credit_card'),
    path('credit_cards/create', CreateCreditCardView.as_view(), name='create_credit_card'),
    
    path('bookings/all', ListAPIView.as_view(queryset=Booking.objects.all(), serializer_class=BookingSerializer), name='index_booking'),
    path('bookings/<int:id>/retrieve', RetrieveBookingView.as_view(), name='retrieve_booking'),
    path('bookings/acknowledge', AcknowledgeBookingView.as_view(), name='acknowledge_booking'),
    path('bookings/create', CreateBookingView.as_view(), name='create_booking'),
    
    path('cleaners/<int:id>/retrieve', RetrieveCleanerView.as_view(), name='retrieve_cleaner'),
    path('cleaners/<int:id>/destroy', DestroyCleanerView.as_view(), name='delete_cleaner'),
    path('cleaners/create', CreateCleanerView.as_view(), name='create_cleaner'),
    path('clean_types/<int:id>/retrieve', RetrieveCleanTypeView.as_view(), name='retrieve_clean_type'),
    path('clean_types/<int:id>/destroy', DestroyCleanTypeView.as_view(), name='delete_clean_type'),
    path('clean_types/create', CreateCleanTypeView.as_view(), name='create_clean_type'),
]