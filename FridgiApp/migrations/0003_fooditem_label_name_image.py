# Generated by Django 4.2.1 on 2023-06-26 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FridgiApp', '0002_foodlistimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodItem_Label_Name_Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
                ('food_item_name', models.CharField(blank=True, max_length=50, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='food_itemimages/')),
            ],
        ),
    ]
