
from rest_framework import serializers
from ..models import ExpenseModel


class ExpenseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseModel
        fields = '__all__'