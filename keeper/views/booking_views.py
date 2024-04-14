from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import Booking
from ..serializers.booking_serializers import BookingSerializer, CreateBookingSerializer, AcknowledgeBookingSerializer

# Create your views here.
class UserBookingsView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    
    def get(self, request):
        user = request.user
        bookings = Booking.objects.filter(user=user)
        serializer = self.serializer_class(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RetrieveBookingView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    lookup_field = 'id'
    
class CreateBookingView(GenericAPIView):
    serializer_class = CreateBookingSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            booking_response = serializer.save()
            return Response(booking_response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AcknowledgeBookingView(GenericAPIView):
    serializer_class = AcknowledgeBookingSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            acknowledgement_response = serializer.save()
            return Response(acknowledgement_response, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    