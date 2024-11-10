
from rest_framework import serializers
from ..models import StaffUserSalaryModel


class StaffUserSalaryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffUserSalaryModel
        fields = '__all__'

    def create(self, validated_data):
        salary = StaffUserSalaryModel.objects.create(**validated_data)
        salary.save()
        return salary

    def update(self, instance, validated_data):
        instance.staff_user = validated_data.get("staff_user", instance.staff_user)
        instance.total_payment = validated_data.get("total_payment", instance.total_payment)
        instance.paid_payment = validated_data.get("paid_payment", instance.paid_payment)
        instance.payment_month = validated_data.get("payment_month", instance.payment_month)
        instance.payment_year = validated_data.get("payment_year", instance.payment_year)
        instance.save()
        return instance
