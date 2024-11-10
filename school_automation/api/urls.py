from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Schema view for Swagger and Redoc
schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()

router.register(r'users', UserModelViewSet, basename="users")
router.register(r'filials', BranchModelViewSet, basename="filials")
router.register(r'rooms', RoomModelViewSet, basename="rooms")
router.register(r'discounts', DicountModelViewSet, basename="discounts")
router.register(r'ads', AdvertisementModelViewSet, basename="ads")
router.register(r'lessons', LessonModelViewSet, basename="lessons")
router.register(r'students', StudentModelViewSet, basename="students")
router.register(r'teachers', TeacherModelViewSet, basename="teachers")
router.register(r'staff_users', StaffUserModelViewSet, basename="staff_users")
router.register(r'groups', GroupModelViewSet, basename="groups")
router.register(r'absences', AbsenceModelViewSet, basename="absences")
router.register(r'group_schedules', GroupScheduleModelViewSet, basename="group_schedules")
router.register(r'student_payments', StudentPaymentModelViewSet, basename="student_payments")
router.register(r'teacher_salary_payments', TeacherSalaryPaymentModelViewSet, basename="teacher_salary_payments")
router.register(r'staff_user_salaries', StaffUserSalaryModelViewSet, basename="staff_user_salaries")
router.register(r'new_students', NewStudentFormModelViewSet, basename="new_students")
router.register(r'expenses', ExpenseModelViewSet, basename="expenses")

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('teachers/teachers_salary/<int:teacher_id>', TeacherModelViewSet.as_view({'get': 'teachers_salary'}), name="teachers_salary"),
    path('new_students/income_outcome/<int:year>', NewStudentFormModelViewSet.as_view({'get': 'income_outcome'}), name="income_outcome"),
]