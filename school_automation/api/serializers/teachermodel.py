from rest_framework import serializers
from ..models import TeacherModel

class TeacherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherModel
        fields = "__all__"
        read_only_fields = ("debt",)  

    def create(self, validated_data):
        lessons=validated_data.pop("subject")
        new_teacher=TeacherModel.objects.create(**validated_data)
        new_teacher.subject.set(lessons)  
        new_teacher.save()
        return new_teacher
    
    def update(self, instance, validated_data):
        lessons = validated_data.pop("subject")
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.subject.clear()
        instance.subject.set(lessons)
        instance.save()
        return instance
    

        
class TeacherModelSpecialSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField()  
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    gender=serializers.CharField()
    address=serializers.CharField()
    image=serializers.ImageField()
    salary_type=serializers.CharField()
    commission=serializers.DecimalField(max_digits=32,decimal_places=2)
    subject= serializers.ListField(
        child=serializers.IntegerField(),  
        allow_empty=False
    )


