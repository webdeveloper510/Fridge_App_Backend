from django.shortcuts import render
from authapp.renderer import UserRenderer
from distutils import errors
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, message
from django.http import JsonResponse
import random
from django.core.mail import send_mail
import datetime
from dateutil.parser import parse as parse_date
# from django.contrib.auth.models import User
from datetime import datetime

#Creating tokens manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
    }
# generate email otp
def generate_email_otp(self):
     otp = random.randint(100000, 999999)
     return otp

class UserRegistrationView(APIView):
 renderer_classes=[UserRenderer]
 def post(self,request,format=None):
    serializer=UserRegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user=serializer.save()
        data={"id":serializer.data['id'],"email":serializer.data['email'],"Firstname":serializer.data['Firstname'],
              "Lastname":serializer.data['Lastname'],"phone_number":serializer.data['phone_number']}
        return Response({'message':'Registation successful','data':data},status=status.HTTP_201_CREATED)
    return Response({errors:serializer.errors},status=status.HTTP_400_BAD_REQUEST)

 
class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        email=request.data.get('email')
        password=request.data.get('password')
        user=authenticate(email=email,password=password)
        
        if user is not None:
            token= get_tokens_for_user(user)
            user_id_data =User.objects.filter(email=email).values('id')
            user_id=user_id_data[0]['id']
            print(user_id)
            return Response({"id":user_id,'message':'Login successful','status':"200","token":token},status=status.HTTP_200_OK)
        else:
            return Response({'message':'Please Enter Valid email or password',"status":"400"},status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class EditCustomerProfile(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(request.user)
        firstname = request.data.get('Firstname')
        lastname = request.data.get('Lastname')
        phone_number = request.data.get('phone_number')
        email = request.data.get('email')
        dob=request.data.get('dob')
        
        try:
            datetime.strptime(dob,'%Y-%m-%d')
        except ValueError:
            return Response({"message": " Date of birth has an invalid format.It must be in YYYY-MM-DD format."}, status=status.HTTP_400_BAD_REQUEST)


        # if not phone_number.isnumeric():
        #     return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': "Enter a valid mobile number"}, status=status.HTTP_400_BAD_REQUEST)

      
        # if len(phone_number) > 15 or len(phone_number) < 10:
        #     return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': "Enter a valid mobile number"}, status=status.HTTP_400_BAD_REQUEST)

        user_data = {}
        if firstname:
            user_data['Firstname'] = firstname
        if lastname:
            user_data['Lastname'] = lastname
        if phone_number:
            user_data['phone_number'] = phone_number
        if email:
            user_data['email'] = email
        if  dob:
            user_data['dob']=dob

        User.objects.filter(id=serializer.data['id']).update(**user_data)

        return Response({"status": status.HTTP_200_OK, "message": "Your profile has been updated successfully"}, status=status.HTTP_200_OK)
   

class ResetPasswordEmail(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        email=request.data.get('email')
    
        if not email:
            return Response({"message":"email is required","status":"400"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not User.objects.filter(email=email).exists():
            return Response({"message":"user with this email does not exists","status":"400"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            otp = generate_email_otp(self)
            created_time= datetime.datetime.now()
            User.objects.filter(email=email).update(email_otp=otp,email_otp_created_time=created_time)
            send_mail(
            'Password Reset OTP',
            f'Your Password Reset Otp for Fridgi:{otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
            return Response({'message':'your password reset otp successfully sent to your email','email':email},status=status.HTTP_200_OK)
        
class OtpView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None): 
        otp=request.data.get('otp')

        if not otp:
            return Response({"message":"otp is required to change the password"},status=status.HTTP_400_BAD_REQUEST)
        
        if not User.objects.filter(email_otp=otp).exists():
            return Response({"message":"please Enter Valid Otp"},status=status.HTTP_400_BAD_REQUEST)
        
        else:
            otp_created_time=User.objects.filter(email_otp=otp).values('email_otp_created_time')
            current_time = datetime.datetime.now()
            time_difference = current_time -parse_date(otp_created_time[0]['email_otp_created_time'])
            if time_difference.total_seconds() > 300:
                return Response({"message":"OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'You entered the correct OTP'}, status=status.HTTP_200_OK)

          


# class ResetPasswordEmail(APIView):
#     renderer_classes=[UserRenderer]
#     def post(self,request,format=None):
#         email=request.data.get('email')

#         if not email:
#             return Response({"message":"email is required","status":"400"}, status=status.HTTP_400_BAD_REQUEST)
        
#         if not User.objects.filter(email=email).exists():
#             return Response({"message":"user with this email does not exists","status":"400"}, status=status.HTTP_400_BAD_REQUEST)

#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             link=" http://127.0.0.1:8000/resetpasswordemail/"
#             subject, from_email, to = 'Reset Your Password', settings.EMAIL_HOST_USER, email
#             text_content = 'This is an important message.'
#             html_content = '<p>Click Following Link to Reset Your Password</p>' + link
#             msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()
#             return JsonResponse({'message':'your password reset link successfully send to your email','status':'200'})


class ResetPassword(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        email=request.data.get('email')
        password=request.data.get('password')
        confirm_password=request.data.get('confirm_password')

        if not email:
            return JsonResponse({'message':'email is required'},status=status.HTTP_400_BAD_REQUEST)
        
        if not  User.objects.filter(email=email).exists():
            return JsonResponse({'message':'email does not exist'},status=status.HTTP_400_BAD_REQUEST)
        
        if not password:
            return JsonResponse({'message':'password is required'},status=status.HTTP_400_BAD_REQUEST)
        
        if not confirm_password:
            return JsonResponse({'message':'confirm your password'},status=status.HTTP_400_BAD_REQUEST)
        
        
        if password!=confirm_password:
            return JsonResponse({'message':'password and confirm password does not match'},status=status.HTTP_400_BAD_REQUEST)
        
        user =User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return JsonResponse({'message':'Reset Password Successfully','status':'200'})


class ProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)


class LogoutUser(APIView):
  renderer_classes = [UserRenderer]
  permission_classes=[IsAuthenticated]
  def post(self, request, format=None):
    return Response({'message':'Logout Successfully','status':status.HTTP_200_OK})
  