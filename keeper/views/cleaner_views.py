from rest_framework.generics import RetrieveAPIView, CreateAPIView, DestroyAPIView
from ..models import Cleaner
from ..serializers.cleaner_serializers import ViewCleanerSerializer, CreateCleanerSerializer, DestroyCleanerSerializer

# Create your views here.
class RetrieveCleanerView(RetrieveAPIView):
    serializer_class = ViewCleanerSerializer
    queryset = Cleaner.objects.all()
    lookup_field = 'id'
    
class DestroyCleanerView(DestroyAPIView):
    lookup_field = 'id'
    queryset = Cleaner.objects.all()
    
class CreateCleanerView(CreateAPIView):
    serializer_class = CreateCleanerSerializer