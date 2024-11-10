from rest_framework import serializers
from ..models import GroupModel
from ..cyberpunks import teachers_salary_1,teachers_salary_2
class GroupModelSerializer(serializers.ModelSerializer):
    number_of_students=serializers.SerializerMethodField(read_only=True)

    def get_number_of_students(self,obj):
        students=obj.students.all()
        return len(students) 
        
        
    class Meta:
        model = GroupModel
        fields = ["id","name","lesson","teacher","students","start_date","status","created_date","number_of_students"]

    def create(self, validated_data):
        students = validated_data.pop("students", [])
        group = GroupModel.objects.create(**validated_data)
        teacher=validated_data.get("teacher")
        if teacher:
            teachers_salary_1(teacher)
        group.students.set(students)
        group.save()
        return group

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.lesson = validated_data.get("lesson", instance.lesson)
        instance.status=validated_data.get("status",instance.status)
        instance.start_date=validated_data.get("start_date",instance.start_date)
        teacher=validated_data.get("teacher")
        if teacher!=instance.teacher:
            teachers_salary_1(teacher)
            teachers_salary_2(instance.teacher,instance)
        instance.teacher = validated_data.get("teacher", instance.teacher)
        instance.students.set(validated_data.get("students", instance.students.all()))
        instance.save()
        return instance
    



