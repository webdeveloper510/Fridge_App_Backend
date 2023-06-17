from django.urls import path
from FridgiApp.views import *
from FridgiApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('food_category/', views.FoodCategoryView.as_view()),
   path('food_category/<int:pk>/', views.FoodCategoryDetail.as_view()),
   path('food_item/', views.FoodItemView.as_view()),
   path('food_item/<int:pk>/', views.FoodItemDetail.as_view()),
   path('food-items/', views.FoodItemTestView.as_view()),
   path('greenIndateitems/', views.GreenInDateItem.as_view()),
   path('expirydateitems/', views.RedExpiryDateItem.as_view()),
   path('usebydate/', views.UseBydateItem.as_view()),
   path('food_itemslist/<int:user_id>/', ItemByUser.as_view(), name='item-by-user'),
   path('food_expireditemslist/<int:user_id>/', ExpiredItemView.as_view(), name='item-by-user'),
   path('textscanner/', views.TextScannerView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)