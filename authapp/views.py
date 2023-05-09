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


#Creating tokens manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
 renderer_classes=[UserRenderer]
 def post(self,request,format=None):
    serializer=UserRegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user=serializer.save()
        return Response({'message':'Registation successful',"status":"201"})
    return Response({errors:serializer.errors},status=status.HTTP_400_BAD_REQUEST)

 
class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        email=request.data.get('email')
        password=request.data.get('password')
        user=authenticate(email=email,password=password)
        if user is not None:
              token= get_tokens_for_user(user)
              return Response({'message':'Login successful','status':"200","token":token})
        else:
               raise serializers.ValidationError({'message':'Please Enter Valid email or password',"status":"400"})

class EditCustomerProfile(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(request.user)
        firstname=request.data.get('firstname')
        lastname=request.data.get('lastname')
        phone_number=request.data.get('phone_number')
        dob=request.data.get('dob')
        clubcard_Number=request.data.get('clubcard_Number')
        
        if not phone_number.isnumeric():
             raise serializers.ValidationError({'status':'status.HTTP_400_BAD_REQUEST','message':"Enter a valid mobile number"})

        if len(phone_number) > 15 or len(phone_number) < 10:
             raise serializers.ValidationError({'status':'status.HTTP_400_BAD_REQUEST','message':"Enter a valid mobile number"})

        if firstname:
            data = User.objects.filter(id=serializer.data['id']).update(Firstname=firstname)
        if lastname:
            data = User.objects.filter(id=serializer.data['id']).update(Lastname=lastname)
        if phone_number:
            data = User.objects.filter(id=serializer.data['id']).update(phone_number=phone_number)
        if dob:
            data = User.objects.filter(id=serializer.data['id']).update(dob=dob)
        if clubcard_Number:
            data = User.objects.filter(id=serializer.data['id']).update(clubcard_Number=clubcard_Number)

        return Response({"status":"200","message":"your profile updated successfully"})   


class ResetPasswordEmail(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        email=request.data.get('email')

        if not email:
            return Response({"message":"email is required","status":"400"})
        
        if not User.objects.filter(email=email).exists():
            return Response({"message":"user with this email does not exists","status":"400"})

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            link=" http://127.0.0.1:8000/resetpasswordemail/"
            subject, from_email, to = 'Reset Your Password', settings.EMAIL_HOST_USER, email
            text_content = 'This is an important message.'
            html_content = '<p>Click Following Link to Reset Your Password</p>' + link
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return JsonResponse({'message':'your password reset link successfully send to your email','status':'200'})


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



class LogoutUser(APIView):
  renderer_classes = [UserRenderer]
  permission_classes=[IsAuthenticated]
  def post(self, request, format=None):
    return Response({'message':'Logout Successfully','status':'status.HTTP_200_OK'})
  