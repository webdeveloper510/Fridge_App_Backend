from rest_framework import serializers
from .models import *

class FoodItemSerializer(serializers.ModelSerializer):
     class Meta:
        model= FoodItem
        fields = '__all__'
           
     def create(self, validate_data):
         return FoodItem.objects.create(**validate_data)

class Food_Category_Serializer(serializers.ModelSerializer):
     class Meta:
        model= Food_Category
        fields = '__all__'
           
     def create(self, validate_data):
         return Food_Category.objects.create(**validate_data)
