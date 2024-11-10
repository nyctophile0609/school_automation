from rest_framework import serializers
from ..models import StaffUserModel
from ..cyberpunks import staff_user_1

class StaffUserModelSerializer(serializers.ModelSerializer):
    class Meta: 
        model = StaffUserModel
        fields = '__all__'

    def create(self, validated_data):
        staff_user = StaffUserModel.objects.create(**validated_data)
        user = staff_user.staff_user
        user.status = "staff_user"
        user.save()
        staff_user.save()
        staff_user_1(staff_user)
        return staff_user

    def update(self, instance, validated_data):
        instance.salary = validated_data.get("salary", instance.salary)
        instance.save()
        staff_user_1(instance)
        return instance
    

        
class StaffModelSpecialSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField()  
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    gender=serializers.CharField()
    address=serializers.CharField()
    image=serializers.ImageField()
    password=serializers.CharField()
    status=serializers.CharField()
    salary=serializers.DecimalField(max_digits=32,decimal_places=2)


