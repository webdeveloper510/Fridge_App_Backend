from django.db import models
from django.db.models import Model


class Food_Category(models.Model):
    food_category=models.CharField(max_length=50, null=True,blank=True)

class FoodItem(models.Model):
    food_category=models.ForeignKey(Food_Category,on_delete=models.CASCADE)
    food_name=models.CharField(max_length=50, null=True,blank=True)
    food_image=models.ImageField(upload_to="food_images/",blank=True,null=True)
    expiry_date=models.DateField()