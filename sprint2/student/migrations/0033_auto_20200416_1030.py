# Generated by Django 3.0.5 on 2020-04-16 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0032_student_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='address_line',
            new_name='elp_score',
        ),
        migrations.RemoveField(
            model_name='student',
            name='euid',
        ),
        migrations.RemoveField(
            model_name='student',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='student',
            name='race',
        ),
        migrations.RemoveField(
            model_name='student',
            name='sat_score',
        ),
        migrations.RemoveField(
            model_name='student',
            name='tofel_score',
        ),
    ]
