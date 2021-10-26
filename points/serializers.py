from rest_framework import serializers
from .models import Point


class PointSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    class Meta:
        model = Point
        fields = ['id', 'owner', 'prize', 'is_confirmed', 'is_donated', 'donated_from', 'donated_to', 'notes', 'is_approved']

    
    def get_owner(self, obj):        
        return obj.owner.username