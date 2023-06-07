# Generated by Django 4.2 on 2023-06-07 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_employee_employeeprofile_remove_saved_jobs_job_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='skill',
            new_name='skills',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='profile_pic',
        ),
        migrations.RemoveField(
            model_name='employeeprofile',
            name='gender',
        ),
        migrations.AddField(
            model_name='employee',
            name='job_type',
            field=models.CharField(choices=[('full time', 'Full Time'), ('part time', 'Part Time'), ('internship', 'Internship'), ('remote', 'Remote')], default='', max_length=100),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='profile_pic',
            field=models.ImageField(default='', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.employeeprofile'),
        ),
    ]
