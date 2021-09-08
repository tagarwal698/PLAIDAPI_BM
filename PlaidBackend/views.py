from django.shortcuts import render
import datetime
import json
import plaid
from django.http import HttpResponse
import requests
from .models import Item
from .tasks import delete_transactions, fetch_transactions
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from .serializers import AccessToken
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .keys import *
from .plaid_client import *
from rest_framework.permissions import IsAuthenticated

def home(request):
    return HttpResponse('<h1>Plaid API and Django REST Framework Asssignment</h2>')

class PublicTokenCreate(APIView):

	def post(self, request):
	# This function is to create a public token
		url = "https://sandbox.plaid.com/sandbox/public_token/create"
		headers = {'content_type', 'application/json'}
		payload = {
			'institution_id': 'ins_s',
			'plaid_public_key': PLAID_PUBLIC_KEY,
			'initial_products': 'transactions'
		}

		r = requests.post(url, data = json.dumps(payload), headers = headers)
		return r.json()


class ExchangeAccessToken(APIView):
	# this function exchanges access token and public token

	permission_classes = [IsAuthenticated]

	def post(self, request):
		public_token = request.data['public_token']

		try:
			# Exchanging tokens
			exchange_response = client.Item.public_token.exchange(public_token) 
			serializer = AccessToken(data = exchange_response)
			
			if serializer.is_valid():
				access_token = serializer.validated_data['access_token']

				item = Item.objects.create(access_token = access_token,
					item_id = serializer.validated_data['item_id'],
					user = self.request.user
					)

				item.save()

				fetch_transactions.delay(access_token)

		except plaid.errors.PlaidError as err:
			return Response(status = status.HTTP_400_BAD_REQUEST)


		return Response(exchange_response, status = status.HTTP_200_OK)


class GetTransactions(APIView):
	# For getting transactions from credit and debit accounts

	permission_classes = [IsAuthenticated]

	def post(self, request):
		item = Item.objects.filter(user = self.request.user)

		if item.count()>0:
			access_token = item[0].access_token

			# getting transactions of last 2 years
			#Getting start date and end date
			start_date = '{%Y-%m-%d}'.format(
				datetime.now() + datetime.timedelta(-730))
			end_date = '{%Y-%m-%d}'.format(datetime.now())

			try:
				transactions_response = client.Transactions.get(
					access_token, start_date, end_date
					)
			except plaid.errors.PlaidError as err:
				return Response(status = status.HTTP_400_BAD_REQUEST)

			return Response(data = {'error':None, 'transactions' : transactions_response}, status = status.HTTP_200_OK)

		else:
			return Response(status = status.HTTP_400_BAD_REQUEST)

class GetIdentity(APIView):
	# Getting information about the identity

	permission_classes = [IsAuthenticated]

	def get(self, request):
		item = Item.objects.filter(user = self.request.user)
		if item.count()>0:
			access_token = item[0].access_token

			try:
				# call for getting the identity response
				identity_response = client.Identity.get(access_token)

			except plaid.errors.PlaidError as err:
				return Response(status = status.HTTP_400_BAD_REQUEST)

			return Response(data = {'error' : None, 'identity' : identity_response}, status = status.HTTP_200_OK)
		else:
			return Response(status= status.HTTP_400_BAD_REQUEST)

class GetBalance(APIView):

	# Getting the balance from a account
	permission_classes = [IsAuthenticated]

	def get(self, request):
		item = Item.objects.filter(user = self.request.user)
		if item.count()>0:
			access_token = item[0].access_token

			try:
				# call for getting the identity response
				balance_response = client.Accounts.balance.get(access_token)

			except plaid.errors.PlaidError as err:
				return Response(status = status.HTTP_400_BAD_REQUEST)

			return Response(data = {'error' : None, 'balance' : balance_response}, status = status.HTTP_200_OK)
		else:
			return Response(status= status.HTTP_400_BAD_REQUEST)


class WebHookTransaction(APIView):

	def post(self, request):
		data = request.data

		webhook_type = data['webhook_type']
		webhook_code = data['webhook_code']

		print(f'{webhook_code} recieved')

		if webhook_type == "TRANSACTIONS":
			item_id = data['item_id']
			if webhook_code == "TRANSACTIONS_REMOVED":
				removed_transactions = data['removed_transactions']
				delete_transactions_from_db.delay(item_id, removed_transactions)
			else:
				new_transactions = data['new_transactions']

				print("New Transaction") 

				save_transactions_to_db.delay(item_id, new_transactions)

		return Response("Webhook Received", status = status.HTTP_200_OK) 

