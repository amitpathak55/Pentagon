# Generated by Django 3.0.4 on 2020-03-23 15:31

from django.db import migrations, models
import student.models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0015_studentfile_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentfile',
            name='link',
        ),
        migrations.AddField(
            model_name='studentfile',
            name='file_link',
            field=models.ImageField(default='123', upload_to=student.models.upload_student_files),
            preserve_default=False,
        ),
    ]