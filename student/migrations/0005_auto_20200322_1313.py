# Generated by Django 3.0.4 on 2020-03-22 13:13

from django.db import migrations, models
import student.models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_student_student_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=student.models.student_image_upload),
        ),
    ]
