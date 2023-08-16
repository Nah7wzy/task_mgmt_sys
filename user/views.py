from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from user.models import User
from user.serializers import UserPublicSerializer, LoginSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from user.utils import Utils
# Create your views here.

class UserPublicAPIView(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserPublicSerializer(user)
        return Response(serializer.data)
    
class LoginView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            user = Utils.authenticate_user(serializer.validated_data)
            
            serialized_user = UserSerializer(user)
            token = Utils.encode_token(user)

            return Response(
                {
                    "data": serialized_user.data,
                    "token": token
                }
            )
           

        except serializers.ValidationError:
            return Response(
                {
                    "message": "Invalid Email or Password"
                }
            )

class SignupView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        data = request.data
        email = data['email']

        serializer = UserSerializer(data=data)
        if serializer.is_valid():

            serializer.save()
            user = User.objects.get(email=email)
            token = Utils.encode_token(user)
            return Response(
                {
                    'data': serializer.data,
                    'token': token
                }
            )

        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                'message': "Invalid Registration Credential"
            }
        )
