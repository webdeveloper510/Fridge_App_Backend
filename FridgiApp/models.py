from django.db import models
from django.db.models import Model
from authapp.models import *


class FoodItem(models.Model):
    name=models.CharField(max_length=50, null=True,blank=True)
    expiry_date=models.DateField(blank=True,null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

class FoodListImage(models.Model):
    image=models.ImageField(upload_to="foodlist_images/",blank=True,null=True)

class FoodItem_Label_Name_Image(models.Model):
    category=models.CharField(max_length=50, null=True,blank=True)
    food_item_name=models.CharField(max_length=50, null=True,blank=True)
    image=models.ImageField(upload_to="food_itemimages/",blank=True,null=True)

class CaptureImage(models.Model):
    image=models.ImageField(upload_to="capture_image/",blank=True,null=True)