# Generated by Django 5.0.4 on 2024-06-29 11:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodel',
            name='got_recommended_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.advertisementmodel'),
        ),
    ]