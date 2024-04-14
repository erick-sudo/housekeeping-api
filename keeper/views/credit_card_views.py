from rest_framework.generics import GenericAPIView, CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import CreditCard
from ..serializers.credit_card_serializers import ViewCreditCardSerializer, CreateCreditCardSerializer, DestroyCreditCardSerializer

# Create your views here.
class RetrieveCreditCardView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ViewCreditCardSerializer
    
    def get(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK) 
    
class DestroyCreditCardView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DestroyCreditCardSerializer
    queryset = CreditCard.objects.all()
    
class CreateCreditCardView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCreditCardSerializer
    
    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            credit_card_creation_response = serializer.save()
            return Response(credit_card_creation_response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)