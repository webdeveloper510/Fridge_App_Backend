# Generated by Django 4.2.1 on 2023-05-08 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_user_groups_user_user_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
