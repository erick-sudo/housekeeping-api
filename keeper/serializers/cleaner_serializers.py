from main.models import User
from main.exception_handlers import SparkleSyncException

from rest_framework import serializers
from ..models import Cleaner


# Serializers
class ViewCleanerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cleaner
        fields = ['user', 'bio', 'id']
        
class DestroyCleanerSerializer(serializers.ModelSerializer):
    pass
        
class CreateCleanerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    bio = serializers.CharField(max_length=255, min_length=6)
    
    class Meta:
        model = Cleaner
        fields = ['user_id', 'id' 'bio']
    
    def create(self, validated_data):
        try:
            user = User.objects.get(id=validated_data['user_id'])
            if Cleaner.objects.filter(user=user).exists():
                raise SparkleSyncException(detail={'message': "user is already a cleaner"}, failure_code="CONFLICT", status_code=409)
        except User.DoesNotExist:
            raise SparkleSyncException(detail={'message': "user does not exist"}, failure_code="NOT_FOUND", status_code=404)
        
        cleaner = Cleaner.objects.create(user=user, bio=validated_data['bio'])
        cleaner.save()
        return {
            'user_id': user.id,
            'bio': cleaner.bio
        }