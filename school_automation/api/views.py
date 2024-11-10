from rest_framework.response import Response
from rest_framework import status,permissions,authentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import *
from .models import *
from .permissions import *
from .filters import *
from .cyberpunks import *

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
 







class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer








class UserModelViewSet(ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserModelFilter
    



    @action(detail=False, methods=["post"])
    def logout(self,request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





    # def get_permissions(self):

    #     permission_classes=[permissions.AllowAny]
    #     if self.action in ["create","update","delete"]:
    #         permission_classes=[permissions.IsAuthenticated,CanOverpowerObj]
    #     elif self.action=="logout":
    #         permission_classes=[permissions.IsAuthenticated]
    #     return [permission() for permission in permission_classes]








class StudentModelViewSet(ModelViewSet):
    queryset = StudentModel.objects.all()
    serializer_class = StudentModelSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentModelFilter




    @action(detail=False, methods=["post"])
    def add_new_students_to_group(self, request):
        """
        adds new students to existing group
        expects: (students:list(id),group_id:int)
        """
        new_students = request.data.get("students")
        group_id = request.data.get("group_id")
        group = get_object_or_404(GroupModel, id=group_id)
        for i in new_students:
            try:
                print(i)
                shadow = get_object_or_404(NewStudentFormModel, id=i)
                user = UserModel.objects.create(
                    phone_number=shadow.phone_number1,
                    first_name=shadow.first_name,
                    last_name=shadow.last_name,
                    status="student_user",
                    gender=request.data.get("gender"),
                    address=request.data.get("address"),
                )
                user.set_password(shadow.phone_number1)
                user.save()
                student = StudentModel.objects.create(
                    student=user,
                    second_number=shadow.phone_number2,
                    got_recommended_by=shadow.got_recommended_by,
                )
                group.students.add(student)
                student_debt_1(student)
            except Exception as e:
                return Response({"error": str(e)}, status=400)
        return Response({"status": "students added to group successfully"})
    



    @action(detail=False, methods=["post"])
    def add_students_to_group(self, request):
        """
        adds existing students to existing group
        expects: (students:list(id),group_id:int)
        """
        students = request.data.get("students")
        group_id = request.data.get("group_id")
        group = get_object_or_404(GroupModel, id=group_id)
        for i in students:
            try:
                student = get_object_or_404(StudentModel, id=i)
                group.students.add(student)
                student_debt_1(student)
            except Exception as e:
                return Response({"error": str(e)}, status=400)
        return Response({"status": "students added to group successfully"})
    



    @action(detail=False, methods=["post"])
    def remove_students_from_group(self, request):
        """
        removes existing students from existing group
        expects: (students:list(id),group_id:int)
        """
        students = request.data.get("students")
        group_id = request.data.get("group_id")
        group = get_object_or_404(GroupModel, id=group_id)
        for i in students:
            try:
                student = get_object_or_404(StudentModel, id=i)
                group.students.remove(student)
                student_debt_2(student)
            except Exception as e:
                return Response({"error": str(e)}, status=400)
        return Response({"status": "students removed from group successfully"})




    def perform_destroy(self, instance):
        user=instance.student
        user.status=""
        user.save()
        return super().perform_destroy(instance) 
    



    def get_permissions(self):
        if self.action=="add_new_students_to_group":
            permission_classes = [ IfUserExists]
            return [permission() for permission in permission_classes]
        return super().get_permissions()




    def get_serializer_class(self):
        if self.action in ("add_new_students_to_group","remove_students_from_group","add_students_to_group"):
            return StudentModelSpecialSerializer
        return super().get_serializer_class()








class TeacherModelViewSet(ModelViewSet):
    queryset = TeacherModel.objects.all()
    serializer_class = TeacherModelSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeacherModelFilter
    permission_classes=[permissions.AllowAny]




    @action(detail=False,methods=["post"])
    def create_new_teacher(self,request):
        """
        creates new teacher(before creates new user)
        expects: (phone_number, first_name, last_name, gender, address, image, subject, salary_type, commission)
        """
        phone_number=request.data.get("phone_number")
        first_name=request.data.get("first_name")
        last_name=request.data.get("last_name")
        statust="teacher_user"
        gender=request.data.get("gender")
        address=request.data.get("address")
        image=request.FILES.get("image")
        subject=request.data.getlist("subject")
        salary_type=request.data.get('salary_type')
        commission=request.data.get("commission")
        new_user=UserModel.objects.create(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            status=statust,
            image=image,
            gender=gender,
            address=address)
        new_user.set_password(phone_number)
        new_user.save()
        new_teacher=TeacherModel.objects.create(
            teacher=new_user,
            salary_type=salary_type,
            commission=commission,)
        new_teacher.subject.set(subject)
        serializer=TeacherModelSerializer(new_teacher)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




    @action(detail=False,methods=["get"])
    def teachers_salary(self,request,teacher_id=None):
        """
        enter the id of the teacher into url, "techers_salary/<teacher_id>"
        """
        teacher=get_object_or_404(TeacherModel,pk=teacher_id)
        teachers_salary_1(teacher)
        result = TeacherSalaryModel.objects.filter(total=True, teacher_id=teacher_id)
        return Response(result)
    



    def perform_destroy(self, instance):
        user=instance.teacher
        user.status=""
        user.save()
        return super().perform_destroy(instance)



    def get_permissions(self):
        if self.action=="create_new_teacher":
            permission_classes = [ IfUserExists]
            return [permission() for permission in permission_classes]
        return super().get_permissions() 




    def get_serializer_class(self):
        if self.action=="create_new_teacher":
            return TeacherModelSpecialSerializer
        return super().get_serializer_class()








class StaffUserModelViewSet(ModelViewSet):
    queryset = StaffUserModel.objects.all()
    serializer_class = StaffUserModelSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = StaffUserModelFilter




    @action(detail=False, methods=["post"])
    def create_staff(self, request):
        """
        creates new staff(before creates new user)
        expects: (phone_number, first_name, last_name, gender, address, image, salary, password, status)
        """
        phone_number = request.data.get("phone_number")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        password = request.data.get("password")
        image = request.FILES.get("image")
        salary = request.data.get("salary")
        status1=request.data.get("status")
        gender=request.data.get("gender")
        address=request.data.get("address")

        if not (phone_number and first_name and last_name and password and salary):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        new_user = UserModel.objects.create(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            status=status1,
            image=image,
            gender=gender,
            address=address
        )
        new_user.set_password(password)
        new_user.save()

        new_staff = StaffUserModel.objects.create(
            staff_user=new_user,
            salary=salary
        )
        staff_serializer = StaffUserModelSerializer(new_staff)
        return Response(staff_serializer.data, status=status.HTTP_201_CREATED)
    



    def perform_destroy(self, instance):
        user=instance.stuff_user
        user.status=""
        user.save()
        return super().perform_destroy(instance)




    def get_permissions(self):
        if self.action=="create_staff":
            permission_classes = [ IfUserExists]
            return [permission() for permission in permission_classes]
        return super().get_permissions() 




    def get_serializer_class(self):
        if self.action=="create_staff":
            return StaffModelSpecialSerializer
        return super().get_serializer_class()








class BranchModelViewSet(ModelViewSet):
    queryset = BranchModel.objects.all()
    serializer_class = BranchModelSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BranchModelFilter




    # def get_permissions(self):
    #     permission_classes=[permissions.IsAuthenticated,]
    #     if self.action in ["create"]:
    #         permission_classes=[permissions.AllowAny]
    #     elif self.action=="update":
    #         permission_classes=[CanUpdateProfile]
    #     elif self.action=="delete":
    #         permission_classes=[CanOverpowerObj]
    #     return [permission() for permission in permission_classes]








class RoomModelViewSet(ModelViewSet):
    queryset = RoomModel.objects.all()
    serializer_class = RoomModelSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomModelFilter




    # def get_permissions(self):
    #     permission_classes=[permissions.IsAuthenticated,]
    #     if self.action in ["create","update","delete"]:
    #         permission_classes=[permissions.IsAuthenticated,IsManagerPermission]
    #     return [permission() for permission in permission_classes]








class DicountModelViewSet(ModelViewSet):
    queryset = DiscountModel.objects.all()
    serializer_class = DiscountModelSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DiscountModelFilter




    # def get_permissions(self):
    #     permission_classes=[permissions.IsAuthenticated,]
    #     if self.action in ["create","update","delete"]:
    #         permission_classes=[permissions.nb ,IsManagerPermission]
    #     return [permission() for permission in permission_classes]
 







class AdvertisementModelViewSet(ModelViewSet):
    queryset = AdvertisementModel.objects.all()
    serializer_class = AdvertisementModelSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementModelFilter




    # def get_permissions(self):
    #     permission_classes=[permissions.IsAuthenticated,]
    #     if self.action in ["create","update","delete"]:
    #         permission_classes=[permissions.IsAuthenticated,IsManagerPermission]
    #     return [permission() for permission in permission_classes]
 







class LessonModelViewSet(ModelViewSet):
    queryset = LessonModel.objects.all()
    serializer_class = LessonModelSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = LessonModelFilter




    # def get_permissions(self):
    #     permission_classes=[permissions.IsAuthenticated]
    #     if self.action in ["create","update","delete"]:
    #         permission_classes=[permissions.IsAuthenticated,IsManagerPermission]
    #     return [permission() for permission in permission_classes]
 







class GroupModelViewSet(ModelViewSet):
    queryset = GroupModel.objects.all()
    serializer_class = GroupModelSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = GroupModelFilter








class AbsenceModelViewSet(ModelViewSet):
    queryset = AbsenceModel.objects.all()
    serializer_class = AbsenceModelSerializer
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AbsenceModelFilter




    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)








class GroupScheduleModelViewSet(ModelViewSet):
    queryset = GroupScheduleModel.objects.all()
    serializer_class = GroupScheduleModelSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = GroupScheduleModelFilter




    # @action(detail=False, methods=["post"])
    # def create_group_schedule(self, request):
    #     """
    #     creates group 
    #     """
    #     group_id = request.data.get("group_id")
    #     schedule = request.data.get("schedule", [])

    #     if not group_id or not schedule:
    #         return Response(
    #             {"error": "group_id and schedule are required."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     for item in schedule:
    #         GroupScheduleModel.objects.create(
    #             group_id=group_id,
    #             room=item.get("room"),
    #             day=item.get("day"),
    #             start_time=item.get("start_time"),
    #             end_time=item.get("end_time")
    #         )

    #     return Response(status=status.HTTP_201_CREATED)


    # def get_serializer_class(self):

    #     return super().get_serializer_class()







class StudentPaymentModelViewSet(ModelViewSet):
    serializer_class = StudentPaymentModelSerializer
    authentication_classes = [JWTAuthentication]
    queryset=StudentPaymentModel.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentPaymentModelFilter




    def list(self, request, *args, **kwargs):
        students = StudentModel.objects.all()
        for student in students: 
            student_debt_1(student)
        return super().list(request, *args, **kwargs)








class TeacherSalaryPaymentModelViewSet(ModelViewSet):
    queryset = TeacherSalaryModel.objects.all()
    serializer_class = TeacherSalaryPaymentModelSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeacherSalaryPaymentModelFilter








class StaffUserSalaryModelViewSet(ModelViewSet):
    queryset = StaffUserSalaryModel.objects.all() 
    serializer_class = StaffUserSalaryModelSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = StaffUserSalaryModelFilter




    def list(self, request, *args, **kwargs):
        staff_users=StaffUserModel.objects.all()
        for staff_user in staff_users:
            staff_user_1(staff_user)
        return super().list(request, *args, **kwargs)








class NewStudentFormModelViewSet(ModelViewSet):
    queryset=NewStudentFormModel.objects.all()
    serializer_class=NewStudentFormModelSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewStudentFormModelFilter




    @action(detail=False, methods=["get"])
    def advertisement(self,request):
        # advertisement/<advertisement_object_id>/
        objects=AdvertisementModel.objects.all()
        total_result={}
        res1={}
        total1=0
        total2=0
        for amo in objects:
            x={"students":[len(StudentModel.objects.filter(got_recommended_by=amo))],"new_students":[len(NewStudentFormModel.objects.filter(got_recommended_by=amo))]}
            print(x["students"])
            total1+=x["students"][0]
            total2+=x["new_students"][0]
            res1[amo.name]=x
        for i in res1.keys():
            print(res1[i]["students"][0]*100)
            r1=res1[i]["students"][0]*100/max(total1,1)
            r2=res1[i]["new_students"][0]*100/max(1,total2)
            res1[i]["students"].append(r1)             
            res1[i]["new_students"].append(r2)             
        return Response(res1)
        



    @action(detail=False, methods=["get"])
    def lessons_in_numbers(self,request):
        #just get
        objects=LessonModel.objects.all()
        res={}
        total1=0
        total2=0
        for i in objects:
            groups=GroupModel.objects.filter(lesson=i)
            x=y=0
            y=len(NewStudentFormModel.objects.filter(lesson=i))
            for group in groups:
                x+=len(group.students.all())
            total1+=x
            total2+=y
            res[i.name]={"students":[x],"new_students":[y]}

        for j in res.keys():
            r1=res[j]["students"][0]*100/max(total1,1)
            r2=res[j]["new_students"][0]*100/max(total2,1)
            res[j]["students"].append(r1)
            res[j]["new_students"].append(r2)

        return Response(res)





    @action(detail=False,methods=["get"])
    def group_students(self,request):
        #just get
        groups=GroupModel.objects.all()
        res={}
        total=0
        for group in groups:
            x=len(group.students.all())
            total+=x
            res[group.id]=[x]
            
        for i in res.keys():
            r=res[i][0]*100/total
            res[i].append(r)
        
        return Response(res)




    @action(detail=False,methods=["get"],)
    def income_outcome(self,request,year=None):
        # income_outcome/<year>/
        year= year!=None and year or datetime.now().year 
        rs_date=date(year,1,1)
        re_date=date(year,12,31)
        res1={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}
        res2={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}
        res3={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}
        res4={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}

        student_payments=StudentPaymentModel.objects.filter(paid_date__lte=re_date,paid_date__gte=rs_date,)
        for s_payment in student_payments:
            if s_payment.paid_date:

                res1[s_payment.paid_date.month]+=s_payment.paid_payment
        
        teacher_salaries=TeacherSalaryModel.objects.filter(paid_date__lte=re_date,paid_date__gte=rs_date,total=True)
        
        for t_salary in teacher_salaries:
            if t_salary.paid_date:
                res2[t_salary.paid_date.month]+=s_payment.paid_payment
        
        staff_salaries=StaffUserSalaryModel.objects.filter(paid_date__lte=re_date,paid_date__gte=rs_date)
        for s_salary in staff_salaries:
            if s_salary.paid_date:
                res3[s_salary.padi_date.month]+=s_salary.paid_payment
                
        
        expenses=ExpenseModel.objects.filter(created_date__lte=re_date,created_date__gte=rs_date)
        for expense in expenses:
            res4[expense.created_date.month]+=expense.amount
        
        result={"income":res1,"teacher_salary_outcome":res2,"staff_salary_outcome":res3,"expenses":res4}


        return Response(result)








class ExpenseModelViewSet(ModelViewSet):
    queryset=ExpenseModel.objects.all()
    serializer_class=ExpenseModelSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenseModelFilter



