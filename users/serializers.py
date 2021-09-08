from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(
		required = True,
		validators = [UniqueValidator(queryset = User.objects.all())])
	username = serializers.CharField(
		max_length = 100,
		validators = [UniqueValidator(queryset=User.objects.all())])
	password = serializers.CharField(min_length = 8)

	class meta:
		model = User
		fields = ['username','email','password','id']


	def CreateUser(self, validated_data):
		user = User.objects.create_user(validated_data['username'], validated_data['email'],validated_data['password'])
		return user

class UserLoginSerializer(serializers.ModelSerializer):
	username = serializers.CharField(max_length = 300, required = True)
	password = serializers.CharField(required = True, write_only = True)
	class meta:
		model = User
		fields = ['username','password','email']


