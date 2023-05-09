from django.db import models

class Food(models.Model):
    food_category=models.CharField(max_length=50, null=True,blank=True)
    food_name=models.CharField(max_length=50, null=True,blank=True)
    food_image=models.ImageField(upload_to="food_images/",blank=True,null=True)