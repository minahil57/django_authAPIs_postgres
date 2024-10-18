import datetime

from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework import viewsets, status
from django.contrib.auth.hashers import make_password


from .serializers import LoginSerializer, RegisterationSerializer
from .models import User



class LoginView(viewsets.ViewSet):
    """
        post -> create
        get -> list
        get -> retrieve -> localhost/api/user/1
        puth -> update
        delete -> destroy
    """
    def create(self, request):

        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            email = request.data.get('email')
            password = request.data.get('password')
            print("email: ", email)
            user = User.objects.filter(email=email).first()
            print("user: ", user)
            if user: 
                if check_password(password, user.password):
                    jwt_token = RefreshToken.for_user(user)

                    user.refreshToken = str(jwt_token)
                    user.accessToken = str(jwt_token.access_token)
                    user.tokenExpiry = datetime.datetime.fromtimestamp(jwt_token['exp'], tz=datetime.timezone.utc)
                    User.objects.filter(email=user.email).update(
                        refreshToken=user.refreshToken, 
                        accessToken=user.accessToken,
                        tokenExpiry=user.tokenExpiry,
                        creationDate= datetime.datetime.fromtimestamp(jwt_token['iat'], tz=datetime.timezone.utc)
                        )
                    return Response({
                        "status": True,
                        "message": "Login successful",

                        "data": {
                          "refresh_token": user.refreshToken,
                          "access_token": user.accessToken
                        }
                    })
                else:
                    return Response({
                        "status": False,
                        "message": "Invalid password"
                    })
            else:
                return Response({
                    "status": False,
                    "message": "User not found"
                })
        else:
            return Response({
                "status": False,
                "message": serializer.errors
            })

class RegisterView(viewsets.ViewSet):

    def create(self,request):
        print("this function is called")
        data = request.data
        serializer = RegisterationSerializer(data=data)
        if serializer.is_valid():
            user = User.objects.create(
            name=data['name'],
            email=data['email'],
            password=make_password(data['password'])
            )   
            user.save()
            return Response({
                "status": True,
                "message": "Registration successful"
            })
        else:
            return Response({
                "status": False,
                "message": serializer.errors
            })