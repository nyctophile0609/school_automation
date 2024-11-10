from rest_framework import serializers
from ..models import NewStudentFormModel




class NewStudentFormModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewStudentFormModel
        fields = '__all__'