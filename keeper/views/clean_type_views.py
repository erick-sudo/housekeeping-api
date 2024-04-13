from rest_framework.generics import CreateAPIView, DestroyAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from ..models import CleanType
from ..serializers.clean_type_serializers import ViewCleanTypeSerializer, CreateCleanTypeSerializer

# Create your views here.
class RetrieveCleanTypeView(GenericAPIView):
    serializer_class = ViewCleanTypeSerializer
    
    def get(self, request, id):
        serializer = self.serializer_class(data={'id': id})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
class DestroyCleanTypeView(DestroyAPIView):
    lookup_field = 'id'
    queryset = CleanType.objects.all()
    
class CreateCleanTypeView(CreateAPIView):
    serializer_class = CreateCleanTypeSerializer