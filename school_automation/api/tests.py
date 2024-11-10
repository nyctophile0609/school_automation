from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import *
from django.contrib.auth import get_user_model
from datetime import time

# class UserModelAPITest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.list_url = reverse('users-list')
#         self.detail_url = lambda pk: reverse('users-detail', args=[pk])

#         self.sample_user_data = {
#             "phone_number": "1234567890",
#             "first_name": "John",
#             "last_name": "Doe",
#             "gender": "male_user",
#             "status": "student_user",
#             "is_staff": False,
#             "is_active": True
#         }
#         self.user = UserModel.objects.create(**self.sample_user_data)

#     def test_get_user_list(self):
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]["phone_number"], self.sample_user_data["phone_number"])

#     def test_get_user_detail(self):
#         response = self.client.get(self.detail_url(self.user.id))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["phone_number"], self.sample_user_data["phone_number"])
#         self.assertEqual(response.data["first_name"], self.sample_user_data["first_name"])

#     def test_update_user(self):
#         updated_data = {
#             "first_name": "Jane",
#             "last_name": "Smith",
#             "phone_number": self.user.phone_number,  # Ensures unique constraint
#         }
#         response = self.client.patch(self.detail_url(self.user.id), data=updated_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         self.user.refresh_from_db()
#         self.assertEqual(self.user.first_name, updated_data["first_name"])
#         self.assertEqual(self.user.last_name, updated_data["last_name"])

#     def test_delete_user(self):
#         response = self.client.delete(self.detail_url(self.user.id))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(UserModel.objects.filter(id=self.user.id).exists())



class StudentModelViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Creating a user and group for the tests
        self.user = get_user_model().objects.create_user(phone_number="1234567890", password="password")
        self.client.force_authenticate(user=self.user)

        self.group = GroupModel.objects.create(name="Test Group", start_date="2024-01-01")


        # Sample data for testing
        self.lesson = LessonModel.objects.create(name="Math",price=4000000)
        self.advertisement = AdvertisementModel.objects.create(name="Ad1", description="Test Ad")

        self.new_student_form = NewStudentFormModel.objects.create(
            first_name="John",
            last_name="Doe",
            lesson=self.lesson,
            phone_number1="123456789",
            phone_number2="987654321",
            free_days="Mon,Tue",
            free_time1=time(9, 0),  # Example time value
            free_time2=time(10, 0),  # Example time value
            got_recommended_by=self.advertisement,
        )

        self.student_user = UserModel.objects.create(phone_number="4445556666", first_name="Existing", last_name="Student", status="student_user")
        self.student = StudentModel.objects.create(student=self.student_user)

    def test_add_new_students_to_group(self):
        """Test adding new students to an existing group"""
        url ="students/add_new_students_to_group/"
        # print("\n\n\n\n\n",url)   
        data = {
            "students": [self.new_student_form.id],
            "group_id": self.group.id,
            "gender": "male_user",
            "address": "Test Address"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("status", response.data)
        self.assertTrue(StudentModel.objects.filter(student__phone_number="1112223333").exists())
        self.assertIn(self.student, self.group.students.all())

    # def test_add_existing_students_to_group(self):
    #     """Test adding existing students to an existing group"""
    #     url = reverse('studentmodel-add-students-to-group')
    #     data = {
    #         "students": [self.student.id],
    #         "group_id": self.group.id
    #     }
    #     response = self.client.post(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn("status", response.data)
    #     self.assertIn(self.student, self.group.students.all())

    # def test_remove_students_from_group(self):
    #     """Test removing students from an existing group"""
    #     # First, add the student to the group
    #     self.group.students.add(self.student)

    #     url = reverse('studentmodel-remove-students-from-group')
    #     data = {
    #         "students": [self.student.id],
    #         "group_id": self.group.id
    #     }
    #     response = self.client.post(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn("status", response.data)
    #     self.assertNotIn(self.student, self.group.students.all())