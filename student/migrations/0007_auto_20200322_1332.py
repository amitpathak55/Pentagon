# Generated by Django 3.0.4 on 2020-03-22 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_student_nationality'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='address',
            new_name='address_line',
        ),
        migrations.AddField(
            model_name='student',
            name='city',
            field=models.CharField(default='x', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='country',
            field=models.CharField(default='x', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='state',
            field=models.CharField(default='x', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='zip_code',
            field=models.CharField(default='x', max_length=40),
            preserve_default=False,
        ),
    ]