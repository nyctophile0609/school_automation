from rest_framework import serializers
from ..models import StudentPaymentModel


class StudentPaymentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPaymentModel 
        fields = '__all__'
        read_only_fields=[""]

    def create(self, validated_data):
        student_payment = StudentPaymentModel.objects.create(**validated_data)
        student_payment.save()
        return student_payment

    def update(self, instance, validated_data):
        instance.total_payment = validated_data.get("total_payment", instance.total_payment)
        instance.paid_payment = validated_data.get("paid_payment", instance.paid_payment)
        instance.save()
        return instance