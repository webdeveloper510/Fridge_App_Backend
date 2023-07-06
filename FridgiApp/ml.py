import os
import cv2
from PIL import Image
import pytesseract as pt
import matplotlib.pyplot as plt
from skimage import filters
from pytesseract import Output
from skimage.filters import threshold_local


variety_name_list = ['Chicken', 'Beef', 'Lamb', 'Fish', 'Pork', 'Sausages', 'Frankfurters', 'Milk', 'Cheese', 'Eggs', 'Fruit', 'Veg', 'Lettuce', 'Green',
                    'Beans', 'Cucumber', 'Mushrooms', 'Onions', 'Radish', 'Yogurts', 'Butter', 'Bread', 'Cooked_Foods', 'Meats', 'Pasta', 'Rice', 'Ready Meals', 'Veg & Processed Meats',
                    'Mayo', 'Tomato Ketchup', 'Salad Cream', 'Brown Sauce', 'BBQ & Jar Sauces','Pickle', 'Freezer','Meats', 
                    'Veg', 'Fruit', 'Bread', 'Milk', 'Ice Cream', 'Cheese (Grated is best)', 'Butter', 'Cooked Foods','sugar']

Input_image_path="/home/deepika/Desktop/Deepika/FridgeBackend/static/media/capture_image/image_8yCuS24.png"

def imshow(title="image", img=None, size=10):
    h, w = img.shape[0], img.shape[1]
    aspect_ratio = h / w
    plt.figure(figsize=(size * aspect_ratio, size))
    plt.title(title)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()

def remove_noise_and_read_text(image_path):
    Read_input_image=cv2.imread(image_path)
    V=cv2.split(cv2.cvtColor(Read_input_image,cv2.COLOR_BGR2HSV))[2]
    T = threshold_local(V,25,offset=25, method="gaussian")
    thresh=(V>T).astype("uint8")*255
    d = pt.image_to_data(thresh, output_type=Output.DICT)
    n_boxes=len(d['text'])
    for i in range(n_boxes):
        if int(d['conf'][i]>(-1)):
            (x ,y ,w ,h)=(d['left'][i] , d['top'][i],d['width'][i],d['height'][i])
            rect=cv2.rectangle(Read_input_image , (x,y,w,h),(0,0,255),3)
    imshow("Rectange Created Image ", rect)
    extracted_text=pt.image_to_string(thresh)
    matched_varieties = []
    for variety_name in variety_name_list:
        if variety_name.lower() in extracted_text.lower():
            matched_varieties.append(variety_name)
    
    print("Matched Varieties: {}".format(matched_varieties))
remove_noise_and_read_text(image_path=Input_image_path)