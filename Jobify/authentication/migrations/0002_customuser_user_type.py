# Generated by Django 4.2 on 2023-06-01 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('employee', 'Employee'), ('employer', 'Employer')], default='employees', max_length=20),
        ),
    ]
