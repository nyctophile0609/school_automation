from rest_framework import serializers
from ..models import TeacherSalaryModel


class TeacherSalaryPaymentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSalaryModel
        fields = '__all__'

    def create(self, validated_data):
        payment = TeacherSalaryModel.objects.create(**validated_data)
        payment.save()
        return payment

    def update(self, instance, validated_data):
        instance.teacher = validated_data.get("teacher", instance.teacher)
        instance.total_payment = validated_data.get("total_payment", instance.total_payment)
        instance.paid_payment = validated_data.get("paid_payment", instance.paid_payment)
        instance.group = validated_data.get("group", instance.group)
        instance.total = validated_data.get("total", instance.total)
        instance.from_date = validated_data.get("from_date", instance.from_date)
        instance.till_date = validated_data.get("till_date", instance.till_date)
        instance.save()
        return instance