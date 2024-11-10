
from rest_framework import serializers
from ..models import AbsenceModel



class BulkAbsenceModelSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        absences = [AbsenceModel(**item) for item in validated_data]
        return AbsenceModel.objects.bulk_create(absences)

    def update(self, instances, validated_data):
        instance_mapping = {instance.id: instance for instance in instances}
        result = []
        for data in validated_data:
            instance = instance_mapping.get(data['id'], None)
            if instance is None:
                result.append(AbsenceModel(**data))
            else:
                for attr, value in data.items():
                    setattr(instance, attr, value)
                instance.save()
                result.append(instance)
        return result

class AbsenceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsenceModel
        fields = '__all__'
        list_serializer_class = BulkAbsenceModelSerializer