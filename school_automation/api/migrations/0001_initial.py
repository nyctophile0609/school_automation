# Generated by Django 5.0.4 on 2024-08-07 16:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvertisementModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=15, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='BranchModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DiscountModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_percent', models.DecimalField(decimal_places=2, max_digits=10)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=32)),
                ('reason', models.CharField(max_length=400)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('status', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone_number', models.CharField(max_length=20, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('female_user', 'Female'), ('male_user', 'Male')], max_length=20, null=True)),
                ('address', models.CharField(max_length=150, null=True)),
                ('status', models.CharField(choices=[('manager_user', 'Manager'), ('administrator_user', 'Administrator'), ('teacher_user', 'Teacher'), ('student_user', 'Student')], max_length=30, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(default='default/default.png', upload_to='')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['-date_joined'],
            },
        ),
        migrations.CreateModel(
            name='HolidayModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='groupes', to='api.groupmodel')),
            ],
        ),
        migrations.CreateModel(
            name='LessonModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=16)),
                ('description', models.CharField(max_length=300, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('discount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.discountmodel')),
            ],
        ),
        migrations.AddField(
            model_name='groupmodel',
            name='lesson',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lesson', to='api.lessonmodel'),
        ),
        migrations.CreateModel(
            name='NewStudentFormModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number1', models.CharField(max_length=20)),
                ('phone_number2', models.CharField(max_length=20)),
                ('free_days', models.CharField(max_length=7)),
                ('free_time1', models.TimeField()),
                ('free_time2', models.TimeField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('got_recommended_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.advertisementmodel')),
                ('lesson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.lessonmodel')),
            ],
        ),
        migrations.CreateModel(
            name='RoomModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.branchmodel')),
            ],
        ),
        migrations.CreateModel(
            name='GroupScheduleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.groupmodel')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.roommodel')),
            ],
        ),
        migrations.CreateModel(
            name='StaffUserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.DecimalField(decimal_places=2, max_digits=32)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('staff_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='staff_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StaffUserSalaryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_payment', models.DecimalField(decimal_places=2, max_digits=16)),
                ('paid_payment', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('from_date', models.DateField()),
                ('till_date', models.DateField()),
                ('closed', models.BooleanField(default=True)),
                ('paid_date', models.DateField(null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('staff_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.staffusermodel')),
            ],
        ),
        migrations.CreateModel(
            name='StudentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('second_number', models.CharField(max_length=15)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('debt', models.DecimalField(decimal_places=2, default=0, max_digits=32)),
                ('got_recommended_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='advertisement', to='api.advertisementmodel')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
                ('student_discounts', models.ManyToManyField(blank=True, related_name='students_discount', to='api.discountmodel')),
            ],
        ),
        migrations.AddField(
            model_name='groupmodel',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='groups', to='api.studentmodel'),
        ),
        migrations.CreateModel(
            name='AbsenceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('excused', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.groupmodel')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.studentmodel')),
            ],
        ),
        migrations.CreateModel(
            name='StudentPaymentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_payment', models.DecimalField(decimal_places=2, max_digits=16)),
                ('paid_payment', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('closed', models.BooleanField(default=False)),
                ('from_date', models.DateField()),
                ('till_date', models.DateField()),
                ('paid_date', models.DateTimeField(null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('all_discounts', models.ManyToManyField(blank=True, related_name='student_discount', to='api.discountmodel')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.groupmodel')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.studentmodel')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary_type', models.CharField(choices=[('fixed_salary', 'Fixed'), ('commission_based_salary', 'Commission Based')], max_length=30)),
                ('commission', models.DecimalField(decimal_places=2, max_digits=32)),
                ('debt', models.DecimalField(decimal_places=2, default=0, max_digits=32)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('subject', models.ManyToManyField(to='api.lessonmodel')),
                ('teacher', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='groupmodel',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_teacher', to='api.teachermodel'),
        ),
        migrations.CreateModel(
            name='TeacherSalaryPaymentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_payment', models.DecimalField(decimal_places=2, max_digits=16)),
                ('paid_payment', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('total', models.BooleanField(default=False)),
                ('closed', models.BooleanField(default=False)),
                ('from_date', models.DateField()),
                ('till_date', models.DateField()),
                ('paid_date', models.DateTimeField(null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tso_group', to='api.groupmodel')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.teachermodel')),
            ],
        ),
    ]
