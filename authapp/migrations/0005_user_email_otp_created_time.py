# Generated by Django 4.2.1 on 2023-06-19 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_user_email_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_otp_created_time',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
