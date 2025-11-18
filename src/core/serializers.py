from rest_framework import serializers
from .models import Resource

class ResourceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Resource
        fields = ['id','owner','title','data','created_at','updated_at']