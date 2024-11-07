from rest_framework import serializers
from .models import *  
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .cyberpunks import *
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Fetch the user instance
        user = self.user
        
        # Serialize the user instance
        user_data = UserModelSerializer(user).data
        
        # Add custom data to the response
        data['user'] = user_data
        
        return data

    @classmethod
    def get_token(cls, phone_number):
        token = super().get_token(phone_number)
        user=UserModel.objects.filter(phone_number=phone_number)
        users=UserModelSerializer(user)
        return token


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        # Use the parent class to validate the token and get the access token
        data = super().validate(attrs)
        
        # Create a new refresh token
        refresh = RefreshToken(attrs['refresh'])
        
        # Add the new refresh token to the response
        data['refresh'] = str(refresh)
        
        return data



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

class TeacherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherModel
        fields ="__all__"
 
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

class TeacherSalaryPaymentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSalaryPaymentModel
        fields = '__all__'

    def create(self, validated_data):
        payment = TeacherSalaryPaymentModel.objects.create(**validated_data)
        payment.save()
        return payment

    def update(self, instance, validated_data):
        instance.teacher = validated_data.get("teacher", instance.teacher)
        instance.total_payment = validated_data.get("total_payment", instance.total_payment)
        instance.paid_payment = validated_data.get("paid_payment", instance.paid_payment)
        instance.group = validated_data.get("group", instance.group)
        instance.total = validated_data.get("total", instance.total)
        instance.from_date = validated_data.get("from_date", instance.from_date)
        instance.till_date = validated_data.get("till_date", instance.till_date)
        instance.save()
        return instance

class StaffUserSalaryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffUserSalaryModel
        fields = '__all__'

    def create(self, validated_data):
        salary = StaffUserSalaryModel.objects.create(**validated_data)
        salary.save()
        return salary

    def update(self, instance, validated_data):
        instance.staff_user = validated_data.get("staff_user", instance.staff_user)
        instance.total_payment = validated_data.get("total_payment", instance.total_payment)
        instance.paid_payment = validated_data.get("paid_payment", instance.paid_payment)
        instance.payment_month = validated_data.get("payment_month", instance.payment_month)
        instance.payment_year = validated_data.get("payment_year", instance.payment_year)
        instance.save()
        return instance

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

class NewStudentFormModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewStudentFormModel
        fields = '__all__'

class ExpenseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseModel
        fields = '__all__'

class BranchModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchModel
        fields = '__all__'

class RoomModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomModel
        fields = '__all__'

class DiscountModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountModel
        fields = '__all__'

