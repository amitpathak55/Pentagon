# Generated by Django 3.0.4 on 2020-03-24 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0018_auto_20200324_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='advisor',
            field=models.CharField(default='John', max_length=255),
            preserve_default=False,
        ),
    ]
