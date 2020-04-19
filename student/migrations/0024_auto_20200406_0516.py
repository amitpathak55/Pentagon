# Generated by Django 3.0.4 on 2020-04-06 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0023_remove_student_current_academic_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='student',
            name='year',
        ),
        migrations.AddField(
            model_name='student',
            name='starting_semester',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]