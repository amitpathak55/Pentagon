# Generated by Django 3.0.4 on 2020-03-23 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_auto_20200322_1401'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='id',
        ),
        migrations.AddField(
            model_name='student',
            name='current_academic_level',
            field=models.CharField(choices=[('H', 'High School'), ('B', 'Bachelors'), ('M', 'Masters'), ('P', 'PHD')], default='H', max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
