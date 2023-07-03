from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import datetime
from datetime import datetime
from rest_framework import generics
from .tasks import notify_user_task
import cv2
import pytesseract   
from django.conf import settings
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from fuzzywuzzy import fuzz
from rest_framework.views import APIView
from rest_framework.response import Response
from PIL import Image
import io

class ImageCaptureView(APIView):
    def post(self, request):
        
        user_id=request.data.get('user_id')
        
        image = request.data.get('image')

        if not user_id:
            return Response({"message":"user is required"},status=status.HTTP_400_BAD_REQUEST)
        
        
        if not  User.objects.filter(id=user_id).exists():
            return Response({"message":"user does not exist"},status=status.HTTP_400_BAD_REQUEST)


        pil_image = Image.open(image)

        rgba_image = pil_image.convert('RGBA')

        image_stream = io.BytesIO()

        rgba_image.save(image_stream, format='PNG')

        test_image = CaptureImage()
        test_image.image.save('image.png', image_stream)

        test_image.save()
        serializer = CaptureImage_Serializer(test_image)
        input_image_path = str(settings.MEDIA_ROOT) + '/' + str(test_image.image)
        
        # Read image 
        input_image = cv2.imread(input_image_path)
        # Extract text from image 
        extracted_text = pytesseract.image_to_string(input_image) 
       
        # Text preprocessing 
        nltk.download('punkt')
        nltk.download('stopwords')
        tokens = word_tokenize(extracted_text)
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
        stemmer = PorterStemmer()
        stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
        
        queryset = FoodItem_Label_Name_Image.objects.all().values('category', 'food_item_name')
        food_item_names = [item['food_item_name'] for item in queryset]
        
        match_threshold = 80  # Match threshold percentage
        
        matched_items = []
        for token in stemmed_tokens:
            for food_item_name in food_item_names:
                similarity = fuzz.token_set_ratio(token, food_item_name)
                if similarity >= match_threshold:
                    matched_items.append(food_item_name)
        
        if matched_items:
            print("Matched Items:")
            array=[]
            for item in matched_items:
                print(item)
                user = User.objects.get(id=user_id)
                user.user = user
                fooddata=FoodItem.objects.create(user=user,name=item)
                fooddata.save()
                array.append(item)
            return Response({"message":"Item extracted successfuuly","data":array})
        
        else:
            print("No matches found.")
            return Response("No matches found.")
      
# Get User Item by User

class FoodItemByUserView(APIView):
    def get(self, request, user_id):
        food_items = FoodItem.objects.filter(user_id=user_id)
        serializer = FoodItemNameSerializer(food_items, many=True)
        return Response(serializer.data)










    
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
