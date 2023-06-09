from rest_framework import serializers
from .models import *
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str,force_bytes, DjangoUnicodeDecodeError
from authapp.utils import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','password','Firstname','Lastname','phone_number']

        extra_kwargs={
            'email': {'error_messages': {'required': "email is required",'blank':'please provide a email'}},
            'password': {'error_messages': {'required': "password is required",'blank':'please Enter a password'}},
            'Firstname': {'error_messages': {'required': "firstname is required",'blank':'firstname could not blank'}},
            'Lastname': {'error_messages': {'required': "lastname is required",'blank':'lastname could not blank'}},
            'phone_number': {'error_messages': {'required': "phone number is required",'blank':'phone number could not blank'}},
          }
        
    def create(self, validated_data,):
       user=User.objects.create(
       email=validated_data['email'],
       Firstname=validated_data['Firstname'],
       Lastname=validated_data['Lastname'],
       phone_number=validated_data['phone_number'],)
       user.set_password(validated_data['password']) 
       user.save()
       return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','Firstname','Lastname','phone_number']   


