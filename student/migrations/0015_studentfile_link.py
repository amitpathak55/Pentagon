# Generated by Django 3.0.4 on 2020-03-23 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0014_remove_educationhistoy_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentfile',
            name='link',
            field=models.CharField(default='as', max_length=255),
            preserve_default=False,
        ),
    ]
