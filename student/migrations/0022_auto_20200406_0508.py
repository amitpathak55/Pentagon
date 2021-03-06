# Generated by Django 3.0.4 on 2020-04-06 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0021_auto_20200326_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='address_line',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='advisor',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='city',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='country',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='current_academic_level',
            field=models.CharField(blank=True, choices=[('H', 'High School'), ('B', 'Bachelors'), ('M', 'Masters'), ('P', 'PHD')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='euid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(blank=True, choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Other')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='nationality',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.Program'),
        ),
        migrations.AlterField(
            model_name='student',
            name='race',
            field=models.CharField(blank=True, choices=[('AA', 'African American'), ('NA', 'Native American'), ('PI', 'Pacific Islander'), ('AS', 'Asian'), ('NH', 'Native Hawaiian')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='semester',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='state',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='zip_code',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
