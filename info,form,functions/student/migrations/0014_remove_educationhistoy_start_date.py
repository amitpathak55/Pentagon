# Generated by Django 3.0.4 on 2020-03-23 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0013_auto_20200323_1410'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='educationhistoy',
            name='start_date',
        ),
    ]