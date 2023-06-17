from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from django.http import JsonResponse
from rest_framework import status
from django.http import Http404
from django.utils import timezone
import datetime
from datetime import datetime
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .tasks import notify_user_task
import os
import cv2
from PIL import Image
import pytesseract as pt
import matplotlib.pyplot as plt
from skimage import filters
from pytesseract import Output
from skimage.filters import threshold_local


class FoodCategoryView(APIView): 
  
    def get(self, request, format=None):
        foodcategory = Food_Category.objects.all()
        serializer = Food_Category_Serializer(foodcategory, many=True)
        return Response(serializer.data)
  
    def post(self, request, format=None):
        serializer = Food_Category_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FoodCategoryDetail(APIView):
    
    def get_object(self, pk):
    
        try:
            return Food_Category.objects.get(pk=pk)
        except Food_Category.DoesNotExist:
            raise Http404
  
    def get(self, request, pk, format=None):
        foodcategory = self.get_object(pk)
        serializer = Food_Category_Serializer(foodcategory)
        return Response(serializer.data)
  
    def put(self, request, pk, format=None):
        foodcategory = self.get_object(pk)
        serializer = Food_Category_Serializer(foodcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    def patch(self, request, pk, format=None):
        foodcategory = self.get_object(pk)
        serializer = Food_Category_Serializer(foodcategory,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
  
    def delete(self, request, pk, format=None):
        foodcategory = self.get_object(pk)
        foodcategory.delete()
        return Response(status=status.HTTP_200_OK)
    
class FoodItemView(APIView): 
  
    def get(self, request, format=None):
        food_item = FoodItem.objects.all()
        serializer = FoodItemSerializer(food_item, many=True)
        return Response(serializer.data)
  
    def post(self, request, format=None):
        serializer = FoodItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FoodItemDetail(APIView):
    
    def get_object(self, pk):
    
        try:
            return FoodItem.objects.get(pk=pk)
        except FoodItem.DoesNotExist:
            raise Http404
  
    def get(self, request, pk, format=None):
        food_item = self.get_object(pk)
        serializer = FoodItemSerializer(food_item)
        return Response(serializer.data)
  
    def put(self, request, pk, format=None):
        food_item = self.get_object(pk)
        serializer = FoodItemSerializer(food_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    def patch(self, request, pk, format=None):
        food_item = self.get_object(pk)
        serializer = FoodItemSerializer(food_item,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
  
    def delete(self, request, pk, format=None):
        food_item = self.get_object(pk)
        food_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class GreenInDateItem(APIView):
    def get(self, request, format=None):
        current_date = datetime.date.today()
        food_items = FoodItem.objects.all().order_by('id')
        serializer = FoodItemSerializer(food_items, many=True)
        array=[]
        for food_item_data in serializer.data:
            expiry_date_str = food_item_data['expiry_date']
            food_name = food_item_data['food_name']
            expiry_date = datetime.datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
            
            if expiry_date >=current_date:
               print("green",food_name)
               food_list= {"food_name":food_name}
               array.append(food_list)
        return Response(array)

class RedExpiryDateItem(APIView):
    def get(self, request, format=None):
        current_date = datetime.date.today()
        food_items = FoodItem.objects.all().order_by('id')
        serializer = FoodItemSerializer(food_items, many=True)
        array=[]
        for food_item_data in serializer.data:
            expiry_date_str = food_item_data['expiry_date']
            food_name = food_item_data['food_name']
            expiry_date = datetime.datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
            if expiry_date<current_date:
               print("green",food_name)
               food_list= {"food_name":food_name}
               array.append(food_list)
        return Response(array)

class UseBydateItem(APIView):
     def post(self, request, format=None):
         fooditem_id=request.data.get('fooditem_id')
         if not fooditem_id:
             return Response({"message":"food item id is required"},status=status.HTTP_400_BAD_REQUEST)
         food_items = FoodItem.objects.filter(id=fooditem_id).values("food_name","expiry_date")
         item_name=food_items[0]['food_name']
         use_by_date=food_items[0]['expiry_date']
         return Response({"status":"success","food name":item_name,"use_by_date":use_by_date},status=status.HTTP_200_OK)
     
# item by user_id

class ItemByUser(generics.ListAPIView):
    serializer_class = FoodItemSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return FoodItem.objects.filter(user_id=user_id)

# Expired item by user id   

class ExpiredItemView(APIView):
    def get(self, request, user_id):
        expired_items = FoodItem.objects.filter(user=user_id, expiry_date__lt=datetime.now())
        serializer = FoodItemSerializer(expired_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class FoodItemTestView(APIView):
    def post(self, request):
        serializer = FoodItemSerializer(data=request.data)
        print("hii")
        if serializer.is_valid():
            serializer.save()
            expiry_date = serializer.validated_data['expiry_date']
            notify_user_task.apply_async(args=[serializer.data['id']], eta=expiry_date)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import pytesseract
from PIL import Image
import numpy as np
from django.conf import settings

class TextScannerView(APIView):
    def post(self, request):
        image_file = request.FILES.get('image_file')
        Image_data= TextScanner.objects.create(image_file=image_file)
        Image_data.save()
        # image_path="/home/deepika/Desktop/Deepika/FridgeBackend/static/media/scan_images/imagetext.png"
        image = Image.open(image_file)
        image = image.convert('L')
        text = pytesseract.image_to_string(image)
        return Response({"message": "ok", "text": text})
    