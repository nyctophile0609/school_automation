# Generated by Django 5.0.4 on 2024-07-03 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_teachersalarypaymentmodel_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffusersalarymodel',
            name='closed',
            field=models.BooleanField(default=True),
        ),
    ]