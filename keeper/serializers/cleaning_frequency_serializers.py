from rest_framework import serializers
from ..models import CleaningFrequency

class CleaningFrequencySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CleaningFrequency
        fields = '__all__'