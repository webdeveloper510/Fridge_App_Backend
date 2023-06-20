from django.urls import path
from authapp.views import *
from authapp import views


urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('userprofile/', ProfileView.as_view(),name='profile'),
    path('editprofile/',EditCustomerProfile.as_view(),name='edit_profile'),
    path('resetpasswordemail/',ResetPasswordEmail.as_view(),name='send-reset-password email'),
    path('email_otp/',OtpView.as_view()),
    path('resetpassword/',ResetPassword.as_view(),name='reset-password'),
    path('logout/',LogoutUser.as_view(),name='logout'),
]