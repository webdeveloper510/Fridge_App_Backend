from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import datetime
from datetime import datetime
from rest_framework import generics
from .tasks import notify_user_task 
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from fuzzywuzzy import fuzz
from PIL import Image
import io
from rest_framework.exceptions import APIException
import os
import cv2
from PIL import Image
import pytesseract as pt
import matplotlib.pyplot as plt
from skimage import filters
from pytesseract import Output
from skimage.filters import threshold_local
import cv2
from django.conf import settings
nltk.download('punkt')
from nltk.stem.snowball import SnowballStemmer
from fuzzywuzzy import fuzz 
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
Base_url="http://127.0.0.1:8000"



variety_name_list = ['Chicken', 'Beef', 'Lamb', 'Fish', 'Pork', 'Sausages', 'Frankfurters', 'Milk', 'Cheese', 'Eggs', 'Fruit', 'Veg', 'Lettuce', 'Green',
                    'Beans', 'Cucumber', 'Mushrooms', 'Onions', 'Radish', 'Yogurts', 'Butter', 'Bread', 'Cooked_Foods', 'Meats', 'Pasta', 'Rice', 'Ready Meals', 'Veg & Processed Meats',
                    'Mayo', 'Tomato Ketchup', 'Salad Cream', 'Brown Sauce', 'BBQ & Jar Sauces','Pickle', 'Freezer','Meats', 
                    'Veg', 'Fruit', 'Bread', 'Milk', 'Ice Cream', 'Cheese (Grated is best)', 'Butter', 'Cooked Foods','sugar']


def imshow(title="image", img=None, size=10):
    h, w = img.shape[0], img.shape[1]
    aspect_ratio = h / w
    plt.figure(figsize=(size * aspect_ratio, size))
    plt.title(title)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()



class ImageCaptureView(APIView):
    
    def remove_noise_and_read_text(self, image_path,user_id):
        Read_input_image = cv2.imread(image_path)
        V = cv2.split(cv2.cvtColor(Read_input_image, cv2.COLOR_BGR2HSV))[2]
        T = threshold_local(V, 25, offset=25, method="gaussian")
        thresh = (V > T).astype("uint8") * 255
        d = pt.image_to_data(thresh, output_type=Output.DICT)
        n_boxes = len(d['text'])
        for i in range(n_boxes):
            if int(d['conf'][i] > (-1)):
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                rect = cv2.rectangle(Read_input_image, (x, y, w, h), (0, 0, 255), 3)
        imshow("Rectange Created Image ", rect)
        extracted_text = pt.image_to_string(thresh)
        snowBallStemmer = SnowballStemmer("english")
        wordList = nltk.word_tokenize(extracted_text)
        stemWords = [snowBallStemmer.stem(word) for word in wordList]
        matched_varieties = []
        for variety_name in variety_name_list:
            for i in stemWords:
                anc = fuzz.ratio(variety_name.lower() , i)
                if anc > 80:
                    matched_varieties.append(variety_name)

        print("Matched Varieties: {}".format(matched_varieties))
        array=[]
        user = User.objects.get(id=user_id)
        for items in matched_varieties:
            Food_data=FoodItem.objects.create(name=items,user=user)
            serializer=FoodItemNameSerializer(data=Food_data)
            Food_data.save()
            data={"id":Food_data.id,"item":items,"created_at":Food_data.created_at,"last_updated":Food_data.last_updated}
            array.append(data)
        return Response({"messgae":"text extracted succesfully","data":array})

    def post(self, request):
        user_id = request.data.get('user_id')
        image = request.data.get('image')
        if not user_id:
            return Response({"message": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        test_image = CaptureImage()
        test_image.image.save('image.png', image)
        test_image.save()
        serializer = CaptureImage_Serializer(test_image)
        input_image_path = str(settings.MEDIA_ROOT) + '/' + str(test_image.image)

        return self.remove_noise_and_read_text(input_image_path, user_id)


class UpdateFoodItemExpiryDate(APIView):
    def post(self, request, format=None):
        data = request.data.get('data')
        if not data:
            return Response({'message': "You cannot send empty data"}, status=status.HTTP_400_BAD_REQUEST)
        
        for food_data in data:
            item_id = food_data.get('id')
            expiry_date = food_data.get('expiry_date')
            
            if not item_id:
                return Response({"message": "Food item id is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                food_item = FoodItem.objects.get(id=item_id)
            except ObjectDoesNotExist:
                return Response({"message": "Item does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not expiry_date:
                return Response({"message": "Expiry date is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                datetime.strptime(expiry_date, '%Y-%m-%d')
            except ValueError:
                return Response({"message": "Expiry date has an invalid format. It must be in YYYY-MM-DD format."}, status=status.HTTP_400_BAD_REQUEST)
            
            food_item.expiry_date = expiry_date
            food_item.save()
        
        return Response({"message": "Data updated successfully", "status": status.HTTP_200_OK})




from fuzzywuzzy import fuzz

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FoodItem, FoodItem_Label_Name_Image


class FoodItemByUserView(APIView):
    def get(self, request, user_id):
        last_inserted_data = FoodItem.objects.filter(user_id=user_id)

        food_item_names = []
        for item in last_inserted_data:
            food_item_names.append(item.name)

        matched_items = []
        for name in food_item_names:
            for variety_name in variety_name_list:
                ratio = fuzz.ratio(name, variety_name)
                if ratio >= 80:
                    matched_items.append(variety_name)

        matched_item_data = []
        for item in matched_items:
            food_item = FoodItem_Label_Name_Image.objects.filter(food_item_name=item).first()
            if food_item:
                matched_item_data.append({
                    'food_item_name': food_item.food_item_name,
                    'category': food_item.category.category_name if food_item.category else '',
                    'image_url': Base_url + food_item.image.url if food_item.image else ''
                })

        return Response({'message': 'success', 'data': matched_item_data})


    
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











# class FoodCategoryView(APIView): 
  
#     def get(self, request, format=None):
#         foodcategory = Food_Category.objects.all()
#         serializer = Food_Category_Serializer(foodcategory, many=True)
#         return Response(serializer.data)
  
#     def post(self, request, format=None):
#         serializer = Food_Category_Serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,
#                             status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class FoodCategoryDetail(APIView):
    
#     def get_object(self, pk):
    
#         try:
#             return Food_Category.objects.get(pk=pk)
#         except Food_Category.DoesNotExist:
#             raise Http404
  
#     def get(self, request, pk, format=None):
#         foodcategory = self.get_object(pk)
#         serializer = Food_Category_Serializer(foodcategory)
#         return Response(serializer.data)
  
#     def put(self, request, pk, format=None):
#         foodcategory = self.get_object(pk)
#         serializer = Food_Category_Serializer(foodcategory, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
#     def patch(self, request, pk, format=None):
#         foodcategory = self.get_object(pk)
#         serializer = Food_Category_Serializer(foodcategory,
#                                            data=request.data,
#                                            partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
  
#     def delete(self, request, pk, format=None):
#         foodcategory = self.get_object(pk)
#         foodcategory.delete()
#         return Response(status=status.HTTP_200_OK)
    
# class FoodItemView(APIView): 
  
#     def get(self, request, format=None):
#         food_item = FoodItem.objects.all()
#         serializer = FoodItemSerializer(food_item, many=True)
#         return Response(serializer.data)
  
#     def post(self, request, format=None):
#         serializer = FoodItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,
#                             status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class FoodItemDetail(APIView):
    
#     def get_object(self, pk):
    
#         try:
#             return FoodItem.objects.get(pk=pk)
#         except FoodItem.DoesNotExist:
#             raise Http404
  
#     def get(self, request, pk, format=None):
#         food_item = self.get_object(pk)
#         serializer = FoodItemSerializer(food_item)
#         return Response(serializer.data)
  
#     def put(self, request, pk, format=None):
#         food_item = self.get_object(pk)
#         serializer = FoodItemSerializer(food_item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
#     def patch(self, request, pk, format=None):
#         food_item = self.get_object(pk)
#         serializer = FoodItemSerializer(food_item,
#                                            data=request.data,
#                                            partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
  
#     def delete(self, request, pk, format=None):
#         food_item = self.get_object(pk)
#         food_item.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
