# Generated by Django 4.2 on 2023-06-09 04:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0004_employerprofile_email_job_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employerprofile',
            name='email',
            field=models.EmailField(default='', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='employerprofile',
            name='mobile',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='employerprofile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employerprofile', to=settings.AUTH_USER_MODEL),
        ),
    ]
