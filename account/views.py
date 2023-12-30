from django.shortcuts import render
from .models import User
from django.contrib.auth import authenticate
from .serializer import UserRegistration_Serializer,UserLogin_Serializer,UserProfile_Serializer,UserPasswordChange_Serializer
from . import serializer
from rest_framework_simplejwt.tokens import RefreshToken
from rnt.utils import Util
from rnt.render import UserRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics,status,permissions


# generating the token for the user.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

# user registration view.
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistration_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # extracting the id of the registred user.
            uid = user.id
            # email sending after the user is registred and saved.
            data = {
                "subject": "Django Email",
                "body": user.name
                + " "
                + "You have been successfully registred in our Site !!!",
                "to_email": user.email,
            }
            Util.send_email(data)
            token = get_tokens_for_user(user)  # for the token...
            return Response(
                {
                    "token": token,
                    "msg": "Registration Successful",
                    "uid": uid,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# user login view.
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLogin_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            # user_nrmuser = user.is_user
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {
                        "token": token,
                        # "user_is_admin": user_type,
                        "msg": "Login Successfully",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"msg": "Email or Password is not valide"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# login user profile view.
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfile_Serializer(request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    
# user password change view.
class UserPasswordChangeView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserPasswordChange_Serializer(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "Password changed Sucessfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)