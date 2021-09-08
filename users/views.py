from django.shortcuts import render,redirect
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
import requests
from rest_framework.decorators import action
from .serializers import UserLoginSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework.authtoken.serializers import AuthTokenSerializer



class UserRegistrationAPIView(APIView):
	def post(self,request):
		serializer = UserRegistrationSerializer(data = request.data)

		if serializer.is_valid():
			user = serializer.save()
			if user:
				token = Token.objects.create(user = user)
				json = serializer.data
				json['token'] = token.key

				return Response({
					'user':user.username,
					'email':user.email,
					'message':"Account Created"
					},status = status.HTTP_200_OK)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
    	serializer = UserLoginSerializer(request.data)
    	if serializer.is_valid():
    		username = serializer.validated_data['username']
    		password = serializer.validated_data['password']
    		user = authenticate(username = 'username', password='password')

    		if user is None:
    			raise serializers.ValidationError("Invalid Credentials. Please Try Again")
    		else:
    			login(request,user)
    			token,created = Token.objects.get_or_create(user = user)
    			return Response({
    				'token':token.key,
    				'email':user.email
    				},status = status.HTTP_200_OK)

    	return Response(serializers.errors,status = status.HTTP_400_BAD_REQUEST)
			

class UserLogoutAPIView(APIView):
	permission_classes = [IsAuthenticated]
	def get(self,request):
		try:
			request.user.auth_token.delete()
		except (ObjectDoesNotExist):
			return Response(serializers.errors,status = status.HTTP_400_BAD_REQUEST)

		logout(request)
		return Response({
			'success':'Logged Out'
			}, status = status.HTTP_200_OK)




