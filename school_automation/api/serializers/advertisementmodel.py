from rest_framework import serializers
from ..models import AdvertisementModel,StudentModel,NewStudentFormModel


class AdvertisementModelSerializer(serializers.ModelSerializer):

    water_tribe = serializers.SerializerMethodField(read_only=True)
    def get_water_tribe(self, obj):
        qw = StudentModel.objects.filter(got_recommended_by=obj).count()
        wq = NewStudentFormModel.objects.filter(got_recommended_by=obj).count()
        data = {
            "students": qw,
            "new_students": wq,
        }
        return data

    class Meta:
        model = AdvertisementModel
        fields = ["id","name","description","water_tribe","created_date"]