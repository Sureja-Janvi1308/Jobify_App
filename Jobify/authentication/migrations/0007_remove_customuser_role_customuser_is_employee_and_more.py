# Generated by Django 4.2 on 2023-06-09 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_remove_customuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='role',
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_employee',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_employer',
            field=models.BooleanField(default=False),
        ),
    ]
