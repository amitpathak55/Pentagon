# Generated by Django 3.0.4 on 2020-03-26 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0020_auto_20200324_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Program'),
        ),
    ]