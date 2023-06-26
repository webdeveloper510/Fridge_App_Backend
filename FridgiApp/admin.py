from django.contrib import admin
from .models import *


@admin.register(FoodItem_Label_Name_Image)
class FoodItem_Label_Name_ImageAdmin(admin.ModelAdmin):
  list_display = ('id','category','food_item_name','image')

