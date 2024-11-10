from rest_framework import serializers
from ..models import GroupModel, StudentModel

class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = '__all__'
        read_only_fields = ["debt"]

    def create(self, validated_data):
        discounts = validated_data.pop("student_discounts", [])
        student = StudentModel.objects.create(**validated_data)
        user = student.student
        user.status = "student_user"
        user.save()
        for discount in discounts:    
            student.student_discounts.add(discount)
        student.save()
        return student

    def update(self, instance, validated_data):
        instance.second_number = validated_data.get("second_number", instance.second_number)
        discounts = validated_data.pop("student_discounts", [])
        for discount in discounts:    
            instance.student_discounts.add(discount)
        instance.save()
        return instance
    
class StudentModelSpecialSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()  
    students = serializers.ListField(
        child=serializers.IntegerField(),  
        allow_empty=False
    )


