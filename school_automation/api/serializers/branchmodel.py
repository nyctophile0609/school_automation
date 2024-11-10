from rest_framework import serializers
from ..models import BranchModel




class BranchModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchModel
        fields = '__all__'