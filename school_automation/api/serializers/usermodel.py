from rest_framework import serializers
from ..models import UserModel


class UserModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ["id", "phone_number", "first_name", "last_name","gender","address", "status", "password", "image"]
        read_only_fields = ["id", "status"]

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        user.status = ""
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.phone_number=validated_data.get("phone_number",instance.phone_number )
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.image = validated_data.get("image", instance.image)
        instance.address = validated_data.get("address", instance.address)
        instance.gender = validated_data.get("gender", instance.gender)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.save()
        return instance

