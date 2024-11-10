
from rest_framework import serializers
from ..models import LessonModel

class LessonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonModel
        fields = '__all__'

    def create(self, validated_data):
        discount = validated_data.pop("discount", None)
        lesson = LessonModel.objects.create(**validated_data)
        lesson.discount = discount
        lesson.save()
        return lesson

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.price = validated_data.get("price", instance.price)
        instance.description = validated_data.get("description", instance.description)
        instance.discount = validated_data.get("discount", instance.discount)
        instance.save()
        return instance