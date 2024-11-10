from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from datetime import datetime
from .manager import *
import datetime
import os
import shutil
from school_automation.settings import MEDIA_ROOT
from django.http import JsonResponse

USER_STATUS_CHOICES=[("manager_user","Manager"),("administrator_user","Administrator"),
                     ("teacher_user","Teacher"),("student_user","Student")]
DAY_CHOICES = [(0, 'Monday'),(1, 'Tuesday'),(2, 'Wednesday'),
    (3, 'Thursday'),(4, 'Friday'),(5, 'Saturday'),(6, 'Sunday'),]
TEACHER_SALARY_CHOICES=[("fixed_salary","Fixed"),("commission_based_salary","Commission Based")]
STUDENT_STATUS_CHOICES=[("frozen_student","Frozen"),("active_student","Active"),]
GENDER_CHOICES=[("female_user","Female"),("male_user","Male")]

class UserModel(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender=models.CharField(choices=GENDER_CHOICES,max_length=20,null=True)
    address=models.CharField(max_length=150,null=True)
    status = models.CharField(choices=USER_STATUS_CHOICES, max_length=30, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default="default/default.png",null=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image_instance = self.image
        new_directory_path = os.path.join(MEDIA_ROOT, f"user_{self.id}")
        if not os.path.exists(new_directory_path):
            os.makedirs(new_directory_path)
        source_image_path = image_instance.path
        _, file_name = os.path.split(source_image_path)
        new_image_path = os.path.join(new_directory_path, file_name)
        try:
            shutil.move(source_image_path, new_image_path)
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': f"Error moving image file: {e}"}, status=400)
        if self.image != f"user_{self.id}/{file_name}":
            self.image = f"user_{self.id}/{file_name}"
            self.save()

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.phone_number


class BranchModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, null=True)
    created_date = models.DateTimeField(auto_now_add=True)


class RoomModel(models.Model):
    name = models.CharField(max_length=30)
    branch = models.ForeignKey(BranchModel, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)


class DiscountModel(models.Model):
    discount_percent = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)


class AdvertisementModel(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=15, null=True)
    created_date = models.DateTimeField(auto_now_add=True)


class LessonModel(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    description = models.CharField(max_length=300, null=True)
    discount = models.ForeignKey(DiscountModel, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)


class StudentModel(models.Model):
    student = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="student")
    second_number = models.CharField(max_length=15)
    created_date = models.DateTimeField(auto_now_add=True)
    got_recommended_by=models.ForeignKey(AdvertisementModel,null=True,on_delete=models.SET_NULL,related_name="advertisement")
    student_discounts=models.ManyToManyField(DiscountModel,blank=True,related_name="students_discount")
    debt=models.DecimalField(max_digits=32,decimal_places=2,default=0)

class TeacherModel(models.Model):
    teacher = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="teacher")
    subject = models.ManyToManyField(LessonModel)
    salary_type = models.CharField(choices=TEACHER_SALARY_CHOICES, max_length=30)
    commission = models.DecimalField(max_digits=32, decimal_places=2)
    debt=models.DecimalField(max_digits=32,decimal_places=2,default=0)
    created_date = models.DateTimeField(auto_now_add=True)


class StaffUserModel(models.Model):
    staff_user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="staff_user")
    salary = models.DecimalField(max_digits=32, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)


class GroupModel(models.Model):
    name = models.CharField(max_length=100)
    lesson = models.ForeignKey(LessonModel, on_delete=models.SET_NULL, null=True, related_name="lesson")
    teacher = models.ForeignKey(TeacherModel, on_delete=models.SET_NULL, null=True, related_name="group_teacher")
    students = models.ManyToManyField(StudentModel, blank=True, related_name="groups")
    start_date = models.DateField()
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)


class AbsenceModel(models.Model):
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupModel, on_delete=models.CASCADE)
    date = models.DateField()
    excused = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)


class GroupScheduleModel(models.Model):
    group = models.ForeignKey(GroupModel, on_delete=models.CASCADE)
    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_date = models.DateTimeField(auto_now_add=True)


class StudentPaymentModel(models.Model):
    student = models.ForeignKey(StudentModel, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(GroupModel, on_delete=models.SET_NULL, null=True)
    all_discounts = models.ManyToManyField(DiscountModel, related_name="student_discount", blank=True)
    total_payment = models.DecimalField(max_digits=16, decimal_places=2)
    paid_payment = models.DecimalField(max_digits=16, decimal_places=2,default=0)
    closed=models.BooleanField(default=False)
    from_date = models.DateField()
    till_date = models.DateField()
    paid_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)


class TeacherSalaryModel(models.Model):
    teacher = models.ForeignKey(TeacherModel, on_delete=models.SET_NULL, null=True)
    total_payment = models.DecimalField(max_digits=16, decimal_places=2,default=0)
    paid_payment = models.DecimalField(max_digits=16, decimal_places=2,default=0)
    group = models.ForeignKey(GroupModel, on_delete=models.SET_NULL, null=True, related_name="tso_group")
    total = models.BooleanField(default=False)
    closed=models.BooleanField(default=False)
    from_date = models.DateField()
    till_date = models.DateField()
    paid_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)


class StaffUserSalaryModel(models.Model):
    staff_user = models.ForeignKey(StaffUserModel, on_delete=models.SET_NULL, null=True)
    total_payment = models.DecimalField(max_digits=16, decimal_places=2)
    paid_payment = models.DecimalField(max_digits=16, decimal_places=2,default=0)    
    from_date = models.DateField()
    till_date = models.DateField()
    closed=models.BooleanField(default=True)
    paid_date=models.DateField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)


class NewStudentFormModel(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    lesson = models.ForeignKey(LessonModel, on_delete=models.SET_NULL, null=True)
    phone_number1 = models.CharField(max_length=20)
    phone_number2 = models.CharField(max_length=20)
    free_days = models.CharField(max_length=7)
    free_time1 = models.TimeField()
    free_time2 = models.TimeField()
    got_recommended_by = models.ForeignKey(AdvertisementModel, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)


class ExpenseModel(models.Model):
    amount = models.DecimalField(max_digits=32, decimal_places=2)
    reason = models.CharField(max_length=400)
    created_date = models.DateTimeField(auto_now_add=True)


class HolidayModel(models.Model):
    groups = models.ManyToManyField(GroupModel, blank=True, related_name="groupes")
    start_date = models.DateField()
    end_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)