
from rest_framework import serializers
from ..models import CleanType, SubService
from main.exception_handlers import SparkleSyncException
from .booking_serializers import ServiceSerializer

class SubServiceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.IntegerField()


# Serializers
class CleanTypeSerializer(serializers.ModelSerializer):
    sub_services = ServiceSerializer(many=True)
    
    class Meta:
        model = CleanType
        fields = ['id', 'name', 'description', 'sub_services']
    
class ViewCleanTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    
    class Meta:
        model = CleanType
        fields = ['id']
        
    def validate(self, attrs):
        id = attrs.get('id')
        try:
            clean_type = CleanType.objects.get(pk=id)
        except CleanType.DoesNotExist:
            raise SparkleSyncException(detail={'message': "Clean Type not found"}, failure_code="NOT_FOUND", status_code=404)
        
        sub_service_serializer = SubServiceSerializer(clean_type.sub_services.all(), many=True)
        
        return {
            'name': clean_type.name,
            'description': clean_type.description,
            'id': clean_type.id,
            'sub_services': sub_service_serializer.data
        }
        
class CreateCleanTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, min_length=1)
    description = serializers.CharField(max_length=255, min_length=1)
    
    class Meta:
        model = CleanType
        fields = ['name', 'description', 'id']