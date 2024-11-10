from rest_framework import serializers
from ..models import RoomModel

class RoomModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomModel
        fields = '__all__'