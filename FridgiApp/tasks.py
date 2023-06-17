from celery import shared_task
from django.utils import timezone
from datetime import datetime
from FridgiApp.models import *

@shared_task
def notify_user_task(food_item_id):
    food_item = FoodItem.objects.get(id=food_item_id)
    user = food_item.user
    if food_item.expiry_date <= timezone.now().date():
        # send notification to user
        message = f"The food item '{food_item.food_name}' has expired."
        user.notifications.create(message=message, timestamp=datetime.now())









# def start():
#     try:
#         scheduler = BackgroundScheduler()
#         scheduler.add_job(send_request, 'interval', minutes=1)
#         scheduler.start()
#         logger.info('Scheduler started successfully!')
#     except Exception as e:
#         logger.error('Scheduler not started! Error: %s', e)

# def send_request():
#     try:
#         response = requests.post('http://127.0.0.1:8000/food_expireditemslist/')
#         logger.info('API called successfully! Response: %s', response.json())
#     except Exception as e:
#         logger.error('Error while calling API! Error: %s', e)