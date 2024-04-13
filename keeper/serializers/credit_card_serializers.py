from main.models import User
from main.exception_handlers import SparkleSyncException

from rest_framework import serializers
from ..models import CreditCard


# Serializers
class ViewCreditCardSerializer(serializers.Serializer):
    
    class Meta:
        model = CreditCard
        fields = ['cardholder_name', 'card_number' 'expiration_date']
        
    def validate(self, attrs):
        #  Obtain the current user
        request = self.context.get('request')
        user = request.user
        
        if not CreditCard.objects.filter(user=user).exists():
            raise SparkleSyncException(detail={'message': "no credit cards found"}, failure_code="NOT_FOUND", status_code=404)
        
        credit_card = CreditCard.objects.get(user=user)
        
        return {
            'id': credit_card.id,
            'cardholder_name': credit_card.cardholder_name,
            'card_number': f"{credit_card.card_number[:4]}**********{credit_card.card_number[-2:]}",
            'expiration_date': credit_card.expiration_date
        }
        
class DestroyCreditCardSerializer(serializers.ModelSerializer):
    pass
        
class CreateCreditCardSerializer(serializers.Serializer):
    cardholder_name = serializers.CharField(max_length=255)
    card_number = serializers.RegexField(
        regex=r'^[0-9]{16}$',
        error_messages={
            'invalid': 'invalid card number. 16 digits required.'
        }
    )
    expiration_date = serializers.RegexField(
        regex=r'^(0[1-9]|1[0-2])\/?([0-9]{2})$',
        error_messages={
            'invalid': 'a valid expiration should take the format MM/YY'
        }
    )
    cvv = serializers.RegexField(
        regex=r'^[0-9]{3,4}$',
        error_messages={
            'invalid': 'a valid cvv includes 3 or 4 digits.'
        }
    )
    
    
    class Meta:
        model = CreditCard
        fields = ['cardholder_name', 'card_number' 'expiration_date', 'cvv']
    
    def create(self, validated_data):
        #  Obtain the current user
        request = self.context.get('request')
        user = request.user
    
        if CreditCard.objects.filter(user=user).exists():
            raise SparkleSyncException(detail={'message': "you already have a credit card"}, failure_code="CONFLICT", status_code=409)
        
        credit_card = CreditCard.objects.create(
            user=user,
            cardholder_name=validated_data['cardholder_name'],
            card_number=validated_data['card_number'],
            expiration_date=validated_data['expiration_date'],
            cvv=validated_data['cvv']
        )
        return {
            'message': "Credit card added successfully",
            'card': f"{credit_card}"
        }