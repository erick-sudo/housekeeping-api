from rest_framework import serializers
from ..models import Booking, SubService, CleaningFrequency, PaymentMethod, CreditCard, AccessInfo
from main.models import User
from main.exception_handlers import SparkleSyncException

# Serializers
class AccessInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessInfo
        fields = ['address_name', 'address_code', 'how_to_get_in', 'any_pets', 'pets_description', 'additional_notes']
        
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubService
        fields = ['id', 'name', 'price']
        
class BookingSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True)
    access_info = AccessInfoSerializer()
    
    class Meta:
        model = Booking
        fields = ['id', 'start_date', 'end_date', 'start_time', 'end_time', 'status', 'user', 'cleaning_frequency', 'payment', 'services', 'cleaners', 'access_info']
        
class CreateBookingSerializer(serializers.ModelSerializer):
    services = serializers.ListField(child=serializers.IntegerField(), min_length=1)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    cleaning_frequency_id = serializers.IntegerField(min_value=1)
    access_info = AccessInfoSerializer()
    
    class Meta:
        model = Booking
        fields = ['services', 'start_date', 'end_date', 'start_time', 'end_time', 'cleaning_frequency_id']
        
    def validate(self, attrs):
        services = attrs.get('services')
        cleaning_frequency_id = attrs.get('cleaning_frequency_id')
        
        for service in services:
            if not SubService.objects.filter(id=service).exists():
                raise SparkleSyncException(detail={'message': "service does not exist"}, failure_code="NOT_FOUND", status_code=404)
            
        if not CleaningFrequency.objects.filter(id=cleaning_frequency_id).exists():
            raise SparkleSyncException(detail={'message': "frequency does not exist"}, failure_code="NOT_FOUND", status_code=404)
        
        return attrs
    
    def create(self, validated_data):
        #  Obtain the current user
        request = self.context.get('request')
        user = request.user
        
        services = SubService.objects.filter(id__in=validated_data['services'])
        cleaning_frequency = CleaningFrequency.objects.get(id=validated_data['cleaning_frequency_id'])
        
        access_info = AccessInfo.objects.create(
            address_name=validated_data['access_info']['address_name'],
            address_code=validated_data['access_info']['address_code'],
            how_to_get_in=validated_data['access_info']['how_to_get_in'],
            any_pets=validated_data['access_info']['any_pets'],
            pets_description=validated_data['access_info']['pets_description'],
            additional_notes=validated_data['access_info']['additional_notes']
        )
        
        booking = Booking.objects.create(
            user=user,
            start_date=validated_data['start_date'],
            end_date=validated_data['end_date'],
            start_time=validated_data['start_time'],
            end_time=validated_data['end_time'],
            cleaning_frequency=cleaning_frequency,
            access_info=access_info
        )
        
        booking.services.set(services)
        booking.save()
        
        return {
            'message': 'Order placed successfully. Wait for an acknowledgement request.',
            'order': f"{booking}",
        }
        
class AcknowledgeBookingSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField(min_value=1)
    payment_method_id = serializers.IntegerField(min_value=1)
    credit_card_id = serializers.IntegerField(min_value=1, required=False)
    
    
    class Meta:
        fields = ['booking_id', 'payment_method_id']
        
    def validate(self, attrs):
        booking_id = attrs.get('booking_id')
        payment_method_id = attrs.get('payment_method_id')
        if not Booking.objects.filter(id=booking_id).exists():
            raise SparkleSyncException(detail={'message': "booking does not exist"}, failure_code="NOT_FOUND", status_code=404)
        
        if not PaymentMethod.objects.filter(id=payment_method_id).exists():
            raise SparkleSyncException(detail={'message': "invalid payment method"}, failure_code="NOT_FOUND", status_code=404)
        
        return attrs
    
    def create(self, validated_data):
        #  Obtain the current user
        request = self.context.get('request')
        user = request.user
        
        booking = Booking.objects.get(id=validated_data['booking_id'])
        payment_method = PaymentMethod.objects.get(id=validated_data['payment_method_id'])
        
        if booking.status != "Pending":
            raise SparkleSyncException(detail={'message': "order already acknowledged"}, failure_code="CONFLICT", status_code=409)
        
        if payment_method.id == PaymentMethod.objects.get(name="Credit Card").id:
            try:
                if not CreditCard.objects.filter(id=validated_data['credit_card_id']).exists():
                    raise SparkleSyncException(detail={'message': "invalid credit card"}, failure_code="NOT_FOUND", status_code=404)
            except KeyError:
                raise SparkleSyncException(detail={'message': "you must provide a valid credit card"}, failure_code="BAD_REQUEST", status_code=400)
            
            credit_card = CreditCard.objects.get(id=validated_data['credit_card_id'])
            
            if CreditCard.objects.filter(user=user).exists():
                users_credit_card = CreditCard.objects.get(user=user)
                if credit_card.id != users_credit_card.id:
                    raise SparkleSyncException(detail={'message': "invalid credit card"}, failure_code="FORBIDDEN", status_code=403)
                
        booking.status = 'Accepted'
        booking.payment = payment_method
        booking.save()
        
        return {
            'message': 'Order acknowledged successfully.',
            'order': f"{booking}",
        }