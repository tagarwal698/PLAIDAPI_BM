from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Account, Item, Transaction

class AccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ['item','account-id','name','current_balance','available_balance','account_type','account_subtype']


class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields = ['account','transaction_id','amount','date','name','payment_mode']


class AccessToken(serializers.ModelSerializer):
	access_token = serializers.CharField(max_length = 100, required = True)
	item_id = serializers.CharField(max_length = 100, required = True)