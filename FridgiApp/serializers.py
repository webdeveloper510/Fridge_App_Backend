from rest_framework import serializers
from .models import *

class FoodItemSerializer(serializers.ModelSerializer):
     class Meta:
        model= FoodItem
        fields = '__all__'
           
     def create(self, validate_data):
         return FoodItem.objects.create(**validate_data)


class CaptureImage_Serializer(serializers.ModelSerializer):
     class Meta:
        model= CaptureImage
        fields = '__all__'
           
     def create(self, validate_data):
         return CaptureImage.objects.create(**validate_data)
    

class FoodItemNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['name']
