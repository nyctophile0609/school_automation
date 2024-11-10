import django_filters
from .models import *

class UserModelFilter(django_filters.FilterSet):
    class Meta:
        model = UserModel
        fields = ['phone_number', 'first_name', 'last_name', 'status', 'is_staff',"gender","address", 'is_active', 'date_joined', ]

class BranchModelFilter(django_filters.FilterSet):
    class Meta:
        model = BranchModel
        fields = ['name', 'description', 'created_date']

class RoomModelFilter(django_filters.FilterSet):
    class Meta:
        model = RoomModel
        fields = ['name', 'branch', 'created_date']
    
class DiscountModelFilter(django_filters.FilterSet):
    class Meta:
        model = DiscountModel
        fields = ['discount_percent', 'start_date', 'end_date', 'created_date']

class AdvertisementModelFilter(django_filters.FilterSet):
    class Meta:
        model = AdvertisementModel
        fields = ['name', 'description', 'created_date']

class LessonModelFilter(django_filters.FilterSet):
    class Meta:
        model = LessonModel
        fields = ['name', 'price', 'description', 'discount', 'created_date']

class StudentModelFilter(django_filters.FilterSet):
    class Meta:
        model = StudentModel
        fields = ['student', 'second_number', 'created_date']

class TeacherModelFilter(django_filters.FilterSet):
    class Meta:
        model = TeacherModel
        fields = ['teacher', 'subject', 'salary_type', 'commission', 'created_date']

class StaffUserModelFilter(django_filters.FilterSet):
    class Meta:
        model = StaffUserModel
        fields = ['staff_user', 'salary', 'created_date']

class GroupModelFilter(django_filters.FilterSet):
    class Meta:
        model = GroupModel
        fields = ['name', 'lesson', 'teacher', 'students', 'start_date', 'status', 'created_date']

class AbsenceModelFilter(django_filters.FilterSet):
    class Meta:
        model = AbsenceModel
        fields = ['student', 'group', 'date', 'excused', 'created_date']

class GroupScheduleModelFilter(django_filters.FilterSet):
    class Meta:
        model = GroupScheduleModel
        fields = ['group', 'room', 'day', 'start_time', 'end_time', 'created_date']

class StudentPaymentModelFilter(django_filters.FilterSet):
    class Meta: 
        model = StudentPaymentModel
        fields = ['student', 'group', 'all_discounts', 'total_payment', 'paid_payment', 'from_date', 'till_date', 'paid_date', 'created_date']

class TeacherSalaryPaymentModelFilter(django_filters.FilterSet):
    class Meta:
        model = TeacherSalaryModel
        fields = ['teacher', 'total_payment', 'paid_payment', 'group', 'total', 'from_date', 'till_date', 'paid_date', 'created_date']

class StaffUserSalaryModelFilter(django_filters.FilterSet):
    class Meta:
        model = StaffUserSalaryModel
        fields = ['staff_user', 'total_payment', 'paid_payment', 'from_date', 'till_date', 'created_date']

class NewStudentFormModelFilter(django_filters.FilterSet): 
    class Meta:
        model = NewStudentFormModel
        fields = ['first_name', 'last_name', 'lesson', 'phone_number1', 'phone_number2', 'free_days', 'free_time1', 'free_time2', 'got_recommended_by', 'created_date']

class ExpenseModelFilter(django_filters.FilterSet):
    class Meta:
        model = ExpenseModel
        fields = ['amount', 'reason', 'created_date']

class HolidayModelFilter(django_filters.FilterSet):
    class Meta:
        model = HolidayModel
        fields = ['groups', 'start_date', 'end_date', 'created_date']

# class StudentFilter(filters.FilterSet):
#     total_paid_min = filters.NumberFilter(field_name="total_paid", lookup_expr='gte')
#     total_paid_max = filters.NumberFilter(field_name="total_paid", lookup_expr='lte')
#     total_debt_min = filters.NumberFilter(field_name="total_debt", lookup_expr='gte')
#     total_debt_max = filters.NumberFilter(field_name="total_debt", lookup_expr='lte')
#     group = filters.CharFilter(method='filter_by_group')

#     class Meta:
#         model = StudentModel
#         fields = ['student_status', 'total_paid_min', 'total_paid_max', 'total_debt_min', 'total_debt_max', 'group']

#     def filter_by_group(self, queryset, name, value):
#         return queryset.filter(groups__name__icontains=value)



# class StudentPaymentFilter(filters.FilterSet):
#     student = filters.CharFilter(method="filter_by_phone_number")

#     group = filters.CharFilter(method='filter_by_group')
#     payment_amount1 = filters.NumberFilter(field_name="payment_amount", lookup_expr='gte')
#     payment_amount2 = filters.NumberFilter(field_name="payment_amount", lookup_expr='lte')
#     payment_year = filters.NumberFilter(field_name="payment_year")
#     payment_month = filters.NumberFilter(field_name="payment_month")
#     paid_date1 = filters.DateTimeFilter(field_name="paid_date", lookup_expr="gte")
#     paid_date2 = filters.DateTimeFilter(field_name="paid_date", lookup_expr="lte")

#     class Meta:
#         model = StudentPaymentModel
#         fields = ['student', 'group', 'payment_amount1', 'payment_amount2', 'payment_year', 'payment_month', 'paid_date1', 'paid_date2']

#     def filter_by_group(self, queryset, name, value):
#         return queryset.filter(group__name__icontains=value)

#     def filter_by_phone_number(self, queryset, name, value):
#         return queryset.filter(student__phone_number__icontains=value)
 

