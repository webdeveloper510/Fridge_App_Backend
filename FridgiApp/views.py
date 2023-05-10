from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from django.http import JsonResponse
from rest_framework import status
from django.http import Http404

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
        return Response(status=status.HTTP_204_NO_CONTENT)
    


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