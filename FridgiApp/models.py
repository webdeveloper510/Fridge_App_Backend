from django.db import models
from django.db.models import Model
from authapp.models import *



class Food_Category(models.Model):
    food_category=models.CharField(max_length=50, null=True,blank=True)


class FoodItem(models.Model):
    food_category=models.ForeignKey(Food_Category,on_delete=models.CASCADE)
    food_name=models.CharField(max_length=50, null=True,blank=True)
    food_image=models.ImageField(upload_to="food_images/",blank=True,null=True)
    expiry_date=models.DateField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)

class Notification(models.Model):
    notification=models.CharField(max_length=250, null=True,blank=True)

class TextScanner(models.Model):
    image_file=models.ImageField(upload_to="scan_images/",blank=True,null=True)

class FoodListImage(models.Model):
    image=models.ImageField(upload_to="foodlist_images/",blank=True,null=True)

class FoodItem_Label_Name_Image(models.Model):
    category=models.CharField(max_length=50, null=True,blank=True)
    food_item_name=models.CharField(max_length=50, null=True,blank=True)
    image=models.ImageField(upload_to="food_itemimages/",blank=True,null=True)