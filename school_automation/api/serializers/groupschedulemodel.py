from rest_framework import serializers
from ..models import GroupScheduleModel

class GroupScheduleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupScheduleModel
        fields = '__all__'

    def create(self, validated_data):
        schedule = GroupScheduleModel.objects.create(**validated_data)
        schedule.save()
        return schedule

    def update(self, instance, validated_data):
        instance.group = validated_data.get("group", instance.group)
        instance.room = validated_data.get("room", instance.room)
        instance.day = validated_data.get("day", instance.day)
        instance.start_time = validated_data.get("start_time", instance.start_time)
        instance.end_time = validated_data.get("end_time", instance.end_time)
        instance.save()
        return instance
    
class ScheduleItemSerializer(serializers.Serializer):
    room = serializers.CharField()
    day = serializers.CharField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

class GroupScheduleModelSpecialSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()
    schedule = serializers.ListField(
        child=ScheduleItemSerializer(),
        allow_empty=False
    )